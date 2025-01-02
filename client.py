import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def receive_messages(client_socket, node_id):
    while True:
        message = client_socket.recv(1024).decode()
        if message:
            sender_id, recipient_id, text = message.split(':')
            if recipient_id == str(node_id):
                print(f"Node {node_id} received: {text} from Node {sender_id}")
            else:
                print(f"Node {node_id} discarded message from Node {sender_id} meant for Node {recipient_id}")

def start_client(node_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionRefusedError:
        print(f"Connection to {SERVER_HOST}:{SERVER_PORT} refused.")
        return

    threading.Thread(target=receive_messages, args=(client_socket, node_id), daemon=True).start()

    while True:
        recipient_id = input(f"Node {node_id}, enter the recipient node ID: ")
        text = input("Enter your message: ")
        message = f"{node_id}:{recipient_id}:{text}"
        client_socket.send(message.encode())

if __name__ == "__main__":
    node_id = int(input("Enter node ID (1-5): "))
    start_client(node_id)
