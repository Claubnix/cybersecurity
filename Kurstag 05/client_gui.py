import sys
import os
import base64
import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QTextEdit, QMessageBox)

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

# Function for AES-256 encryption
def encrypt(plain_text: str, password: str) -> str:
    salt = os.urandom(16)  # Generate random salt
    key = derive_key(password, salt)
    iv = os.urandom(16)  # Random initialization vector (IV)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Add padding
    padded_data = pad(plain_text.encode())
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return salt, IV, and encrypted data in base64-encoded form
    return base64.b64encode(salt + iv + encrypted).decode()

# Padding function for AES encryption
def pad(data: bytes) -> bytes:
    pad_length = 16 - (len(data) % 16)
    return data + bytes([pad_length] * pad_length)

# GUI application
class AESApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-256 Messaging Client")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.label_plaintext = QLabel("Message:")
        self.input_plaintext = QTextEdit()

        self.button_send = QPushButton("Send Encrypted Message")
        self.button_send.clicked.connect(self.send_encrypted_message)

        self.label_result = QLabel("Server Response:")
        self.output_result = QTextEdit()
        self.output_result.setReadOnly(True)

        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_plaintext)
        layout.addWidget(self.input_plaintext)
        layout.addWidget(self.button_send)
        layout.addWidget(self.label_result)
        layout.addWidget(self.output_result)

        self.setLayout(layout)

    def send_encrypted_message(self):
        password = self.input_password.text()
        plain_text = self.input_plaintext.toPlainText()
        if not password or not plain_text:
            QMessageBox.warning(self, "Error", "Please enter password and message.")
            return
        encrypted_text = encrypt(plain_text, password)
        
        try:
            # Send encrypted message to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(('localhost', 12345))
                client_socket.sendall(encrypted_text.encode())
                response = client_socket.recv(1024).decode()
                self.output_result.setPlainText(response)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to send message: {str(e)}")

# Main function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AESApp()
    window.show()
    sys.exit(app.exec())