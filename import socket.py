import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

clients = []

def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

start_server()
