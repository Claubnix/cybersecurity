import socket
import hashlib

# Funktion zur Berechnung der Prüfziffer
def calculate_checksum(message):
    return hashlib.md5(message.encode()).hexdigest()

# Server
def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server läuft und wartet auf Verbindungen...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Verbindung von {addr} akzeptiert.")
        data = conn.recv(1024).decode()
        message, checksum = data.rsplit('|', 1)
        
        if calculate_checksum(message) == checksum:
            print(f"Nachricht empfangen: {message}")
            conn.sendall(b"Nachricht empfangen und verifiziert.")
        else:
            print("Prüfziffer stimmt nicht überein!")
            conn.sendall(b"Fehler: Ungueltige Nachricht.")
        
        conn.close()

# Client
def send_message(host='localhost', port=12345, message="Hallo, Server!"):
    checksum = calculate_checksum(message)
    data = f"{message}|{checksum}"
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(data.encode())
    
    response = client_socket.recv(1024).decode()
    print(f"Serverantwort: {response}")
    
    client_socket.close()

# Beispiel für die Verwendung
if __name__ == "__main__":
    # Starte den Server in einem separaten Thread oder Prozess
    #start_server()

    # Sende eine Nachricht
    send_message(message="Hallo, Server!")