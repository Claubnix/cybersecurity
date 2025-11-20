import socket
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Function to derive a key from a password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 requires a 256-bit key
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function for AES-256 decryption
def decrypt(encrypted_text: str, password: str) -> str:
    # Base64 decode
    encrypted_data = base64.b64decode(encrypted_text)
    
    # Extract salt, IV, and encrypted data
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    encrypted = encrypted_data[32:]
    
    key = derive_key(password, salt)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt and remove padding
    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
    return unpad(decrypted_padded).decode()

# Unpad function for AES decryption
def unpad(data: bytes) -> bytes:
    pad_length = data[-1]
    return data[:-pad_length]

# Server class
class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server is running and waiting for connections...")

    def start(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection accepted from {addr}.")
            data = conn.recv(1024).decode()
            if not data:
                break
            
            # For demonstration, we'll assume the password is known
            password = "my_secure_password"  # Replace with a secure method of handling passwords
            try:
                decrypted_message = decrypt(data, password)
                print(f"Decrypted message: {decrypted_message}")
                conn.sendall(b"Message received and decrypted.")
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                conn.sendall(b"Error in decryption.")
            conn.close()

# Main function
if __name__ == "__main__":
    server = Server()
    server.start()