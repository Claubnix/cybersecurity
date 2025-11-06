from cryptography.fernet import Fernet
import os


def schluessel_generieren_und_speichern(dateiname="secret.key"):
    """Generiert und speichert einen neuen Schlüssel"""
    key = Fernet.generate_key()
    with open(dateiname, 'wb') as key_file:
        key_file.write(key)
    print(f"✓ Neuer Schlüssel in '{dateiname}' gespeichert")
    return key


def schluessel_laden(dateiname="secret.key"):
    """Lädt Schlüssel aus Datei"""
    try:
        with open(dateiname, 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        return None


def verschluesseln_und_speichern(text, key, ausgabe_datei="verschluesselt.txt"):
    """Verschlüsselt Text und speichert in Datei"""
    f = Fernet(key)
    encrypted = f.encrypt(text.encode())

    with open(ausgabe_datei, 'wb') as file:
        file.write(encrypted)

    print(f"✓ Verschlüsselter Text in '{ausgabe_datei}' gespeichert")
    return encrypted


def entschluesseln_aus_datei(key, eingabe_datei="verschluesselt.txt"):
    """Lädt und entschlüsselt Text aus Datei"""
    try:
        with open(eingabe_datei, 'rb') as file:
            encrypted = file.read()

        f = Fernet(key)
        decrypted = f.decrypt(encrypted).decode()
        return decrypted
    except FileNotFoundError:
        print(f"Datei '{eingabe_datei}' nicht gefunden!")
        return None
    except Exception as e:
        print(f"Entschlüsselung fehlgeschlagen: {e}")
        return None


def main():
    print("=== AES Verschlüsselung mit Datei-Schlüssel ===\n")

    key_datei = "mein_schluessel.key"

    # Schlüssel laden oder generieren
    key = schluessel_laden(key_datei)
    if key is None:
        print("Kein Schlüssel gefunden. Generiere neuen...")
        key = schluessel_generieren_und_speichern(key_datei)
    else:
        print(f"✓ Schlüssel aus '{key_datei}' geladen")

    while True:
        print("\nWas möchten Sie tun?")
        print("1 - Text verschlüsseln")
        print("2 - Text entschlüsseln")
        print("3 - Neuen Schlüssel generieren")
        print("4 - Beenden")

        wahl = input("\nIhre Wahl (1-4): ").strip()

        if wahl == "1":
            text = input("Text zum Verschlüsseln eingeben: ")
            if text:
                verschluesseln_und_speichern(text, key)

        elif wahl == "2":
            decrypted = entschluesseln_aus_datei(key)
            if decrypted:
                print(f"Entschlüsselter Text: {decrypted}")

        elif wahl == "3":
            key = schluessel_generieren_und_speichern(key_datei)
            print("WARNUNG: Alter Schlüssel wurde überschrieben!")

        elif wahl == "4":
            print("Auf Wiedersehen!")
            break

        else:
            print("Ungültige Eingabe!")


if __name__ == "__main__":
    main()
