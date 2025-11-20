import sys
import os
import base64
import socket
import threading
# Importe für Kryptografie (verwenden SHA256)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# Importe für PyQt6 GUI
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

# --- Cryptographic Functions (using SHA-256 for Key Derivation) ---

def derive_key(password: str, salt: bytes) -> bytes:
    """Leitet einen 256-Bit-Schlüssel (für AES-256) von einem Passwort ab,
    indem SHA256 und PBKDF2HMAC verwendet werden."""
    # SHA256 wird für die Key Derivation (KDF) verwendet.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 (32 bytes = 256 bit)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def pad(data: bytes) -> bytes:
    """Fügt PKCS7 Padding für AES-Verschlüsselung hinzu."""
    pad_length = 16 - (len(data) % 16)
    return data + bytes([pad_length] * pad_length)

def encrypt(plain_text: str, password: str) -> str:
    """Verschlüsselt den Klartext mit AES-256 CBC und gibt Salt, IV und Daten in Base64 zurück."""
    salt = os.urandom(16)  # Generiert zufälliges Salt (16 Bytes)
    key = derive_key(password, salt)
    iv = os.urandom(16)   # Zufälliger Initialisierungsvektor (IV) (16 Bytes)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padded_data = pad(plain_text.encode('utf-8'))
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Struktur: [16 Bytes Salt] + [16 Bytes IV] + [Verschlüsselte Daten]
    return base64.b64encode(salt + iv + encrypted).decode()

# --- QThread for Network Operations (Prevents GUI blocking) ---

class ClientWorker(QThread):
    # Signale, um Ergebnisse an die GUI zurückzusenden
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, encrypted_data: str, parent=None):
        super().__init__(parent)
        self.encrypted_data = encrypted_data
        self.host = 'localhost'
        self.port = 12345

    def run(self):
        """Führt die blockierende Socket-Kommunikation in einem separaten Thread aus."""
        try:
            # 1. Verbindung herstellen
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                
                # 2. Daten senden (verschlüsselte Base64-Zeichenkette)
                client_socket.sendall(self.encrypted_data.encode('utf-8'))
                
                # 3. Antwort empfangen
                response = client_socket.recv(1024).decode('utf-8')
                
                # Sende die Antwort an das Haupt-GUI-Fenster
                self.finished.emit(response)
                
        except ConnectionRefusedError:
             self.error.emit(f"Verbindung fehlgeschlagen: Der Server ist nicht auf {self.host}:{self.port} erreichbar. Bitte starten Sie 'server.py'.")
        except Exception as e:
            self.error.emit(f"Fehler beim Senden der Nachricht: {type(e).__name__}: {str(e)}")


# --- GUI Application ---

class AESApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-256 Messaging Client (SHA256 KDF)")
        self.setGeometry(100, 100, 450, 400)
        self.worker_thread = None
        
        layout = QVBoxLayout()
        self.setStyleSheet("font-size: 14px;")

        self.label_password = QLabel("Passwort (für AES-256 Key Derivation):")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Das Passwort muss mit dem Serverseitigen übereinstimmen.")

        self.label_plaintext = QLabel("Nachricht (wird verschlüsselt):")
        self.input_plaintext = QTextEdit()
        self.input_plaintext.setPlaceholderText("Ihre Nachricht.")

        self.button_send = QPushButton("Nachricht verschlüsseln und senden")
        self.button_send.clicked.connect(self.start_send_process)
        self.button_send.setStyleSheet("padding: 10px; background-color: #007BFF; color: white; border-radius: 5px;")

        self.label_result = QLabel("Server-Antwort:")
        self.output_result = QTextEdit()
        self.output_result.setReadOnly(True)
        self.output_result.setStyleSheet("background-color: #e9ecef; border: 1px solid #ced4da;")

        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_plaintext)
        layout.addWidget(self.input_plaintext)
        layout.addWidget(self.button_send)
        layout.addWidget(self.label_result)
        layout.addWidget(self.output_result)

        self.setLayout(layout)

    def start_send_process(self):
        """Starts the send process in a separate thread."""
        password = self.input_password.text()
        plain_text = self.input_plaintext.toPlainText()
        
        if not password or not plain_text:
            QMessageBox.warning(self, "Fehler", "Bitte Passwort und Nachricht eingeben.")
            return

        try:
            self.output_result.setPlainText("Verschlüssele Nachricht...")
            encrypted_text = encrypt(plain_text, password)
            self.output_result.append("Verschlüsselung erfolgreich. Sende an Server...")
            
            # Startet den Worker Thread
            self.worker_thread = ClientWorker(encrypted_text, self)
            self.worker_thread.finished.connect(self.handle_success)
            self.worker_thread.error.connect(self.handle_error)
            self.button_send.setEnabled(False) # Deaktiviert den Button während des Sendens
            self.worker_thread.start()

        except Exception as e:
            QMessageBox.critical(self, "Kritischer Fehler", f"Verschlüsselungsfehler: {str(e)}")

    def handle_success(self, response: str):
        """Handles a successful server response."""
        self.output_result.append(f"Server-Antwort erhalten:\n{response}")
        self.button_send.setEnabled(True)

    def handle_error(self, error_message: str):
        """Handles errors occurring in the Worker Thread."""
        QMessageBox.critical(self, "Netzwerkfehler", error_message)
        self.output_result.append(f"Fehler: {error_message}")
        self.button_send.setEnabled(True)

# Main function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AESApp()
    window.show()
    sys.exit(app.exec())