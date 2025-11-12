from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os
import base64

def rsa_schluessel_generieren_und_speichern(private_key_datei="private_key.pem", public_key_datei="public_key.pem"):
    """Generiert RSA-Schlüsselpaar und speichert in Dateien"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    # Private Key speichern
    with open(private_key_datei, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Public Key speichern
    with open(public_key_datei, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    print(f"✓ RSA-Schlüsselpaar generiert und gespeichert")
    return private_key, public_key

def schluessel_laden():
    """Lädt beide Schlüssel"""
    try:
        with open("private_key.pem", 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        
        with open("public_key.pem", 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        
        return private_key, public_key
    except FileNotFoundError:
        return None, None

def verschluesseln_und_speichern(text, public_key, ausgabe_datei="verschluesselt_rsa.txt"):
    """Verschlüsselt Text und speichert in Datei"""
    try:
        encrypted = public_key.encrypt(
            text.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Als Base64 speichern für bessere Lesbarkeit
        with open(ausgabe_datei, 'w') as f:
            f.write(base64.b64encode(encrypted).decode())
        
        print(f"✓ Verschlüsselter Text in '{ausgabe_datei}' gespeichert")
        return encrypted
    except Exception as e:
        print(f"Verschlüsselung fehlgeschlagen: {e}")
        return None

def entschluesseln_aus_datei(private_key, eingabe_datei="verschluesselt_rsa.txt"):
    """Lädt und entschlüsselt Text aus Datei"""
    try:
        with open(eingabe_datei, 'r') as f:
            encrypted_b64 = f.read()
        
        encrypted = base64.b64decode(encrypted_b64)
        
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return decrypted.decode('utf-8')
    except FileNotFoundError:
        print(f"Datei '{eingabe_datei}' nicht gefunden!")
        return None
    except Exception as e:
        print(f"Entschlüsselung fehlgeschlagen: {e}")
        return None

def main():
    print("=== RSA Verschlüsselung mit Datei-Schlüsseln ===\n")
    
    # Schlüssel laden oder generieren
    private_key, public_key = schluessel_laden()
    if private_key is None or public_key is None:
        print("Keine Schlüssel gefunden. Generiere neues RSA-Schlüsselpaar...")
        private_key, public_key = rsa_schluessel_generieren_und_speichern()
    else:
        print("✓ RSA-Schlüsselpaar geladen")
    
    while True:
        print("\nWas möchten Sie tun?")
        print("1 - Text verschlüsseln (mit Public Key)")
        print("2 - Text entschlüsseln (mit Private Key)")
        print("3 - Neues Schlüsselpaar generieren")
        print("4 - Schlüssel-Info anzeigen")
        print("5 - Beenden")
        
        wahl = input("\nIhre Wahl (1-5): ").strip()
        
        if wahl == "1":
            text = input("Text zum Verschlüsseln eingeben (max ~200 Zeichen): ")
            if text:
                if len(text.encode('utf-8')) > 190:  # RSA-2048 Limit mit OAEP
                    print("⚠️  Text zu lang für RSA! Maximal ~190 Bytes.")
                else:
                    verschluesseln_und_speichern(text, public_key)
        
        elif wahl == "2":
            decrypted = entschluesseln_aus_datei(private_key)
            if decrypted:
                print(f"Entschlüsselter Text: {decrypted}")
        
        elif wahl == "3":
            antwort = input("Warnung: Alte Schlüssel werden überschrieben! Fortfahren? (j/n): ")
            if antwort.lower() == 'j':
                private_key, public_key = rsa_schluessel_generieren_und_speichern()
        
        elif wahl == "4":
            print(f"RSA-Schlüsselgröße: {private_key.key_size} Bit")
            print("Dateien:")
            print("  private_key.pem (Privater Schlüssel - GEHEIM!)")
            print("  public_key.pem (Öffentlicher Schlüssel - teilbar)")
        
        elif wahl == "5":
            print("Auf Wiedersehen!")
            break
        
        else:
            print("Ungültige Eingabe!")

if __name__ == "__main__":
    main()