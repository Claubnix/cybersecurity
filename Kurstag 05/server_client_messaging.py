import socket
import threading
import sys
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag, InvalidSignature, InvalidKey

# HINWEIS: In einer echten Anwendung sollte das Passwort NICHT hartkodiert sein!
SHARED_PASSWORD = "Sicherheitsgeheimnis" # Muss mit dem Client-Passwort übereinstimmen

# --- Shared Cryptography Functions ---

def derive_key(password: str, salt: bytes) -> bytes:
    """Leitet den Schlüssel vom Passwort ab (verwendet SHA256)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def unpad(data: bytes) -> bytes:
    """Removes PKCS7 padding."""
    if not data:
        raise ValueError("Data cannot be empty.")
    pad_length = data[-1]
    if not (1 <= pad_length <= 16):
        # Check if the last byte is valid
        raise ValueError("Invalid padding length.")
    return data[:-pad_length]

def decrypt(encrypted_b64: str, password: str) -> str:
    """Decrypts the Base64 data."""
    data = base64.b64decode(encrypted_b64)
    
    # Check if data length is at least Salt (16) + IV (16) = 32 bytes
    if len(data) < 32:
        raise ValueError("Received data is too short for Salt and IV.")

    # Extract Salt (16 bytes) and IV (16 bytes)
    salt = data[:16]
    iv = data[16:32]
    encrypted_data = data[32:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt and remove padding
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    
    decrypted = unpad(decrypted_padded)
    return decrypted.decode('utf-8')

# --- Server Logic ---

def handle_client(conn, addr):
    """Handles the connection of a single client."""
    print(f"[{addr[0]}:{addr[1]}] Verbindung akzeptiert.")
    
    try:
        # 1. Receive the encrypted Base64 data
        encrypted_b64_data = conn.recv(1024).decode('utf-8')
        
        if not encrypted_b64_data:
            print(f"[{addr[0]}:{addr[1]}] Keine Daten empfangen.")
            conn.sendall("Fehler: Leere Nachricht empfangen.".encode('utf-8'))
            return

        # 2. Attempt to decrypt the data
        try:
            decrypted_message = decrypt(encrypted_b64_data, SHARED_PASSWORD)
            
            # 3. Successful Decryption
            print(f"[{addr[0]}:{addr[1]}] Nachricht erfolgreich entschlüsselt: {decrypted_message}")
            response = f"SUCCESS - Nachricht verifiziert. Inhalt: '{decrypted_message}'"
            conn.sendall(response.encode('utf-8'))
            
        except (ValueError, InvalidTag, InvalidSignature, InvalidKey) as crypto_error:
            # 4. Decryption Error (wrong password or tampered data)
            print(f"[{addr[0]}:{addr[1]}] Entschlüsselungsfehler: {type(crypto_error).__name__}. Falsches Passwort oder beschädigte Daten.")
            response = "ERROR - Entschlüsselung fehlgeschlagen (Falsches Passwort oder beschädigte Daten)."
            conn.sendall(response.encode('utf-8'))
            
    except Exception as e:
        print(f"[{addr[0]}:{addr[1]}] Unerwarteter Fehler: {e}")
        conn.sendall("ERROR - Interner Serverfehler.".encode('utf-8'))
        
    finally:
        conn.close()
        print(f"[{addr[0]}:{addr[1]}] Verbindung geschlossen.")

def start_server(host='localhost', port=12345):
    """Starts the multithreaded server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server läuft und wartet auf Verbindungen auf {host}:{port}...")
        print(f"Gemeinsames Passwort ist: '{SHARED_PASSWORD}'")

        while True:
            # Blocks until a client connects
            conn, addr = server_socket.accept() 
            
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
            
    except Exception as e:
        print(f"Kritischer Serverfehler: {e}")
    finally:
        if 'server_socket' in locals() and server_socket:
            server_socket.close()

if __name__ == "__main__":
    start_server()