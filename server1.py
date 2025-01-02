import socket

def main(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', port))
        server_socket.listen(1)
        print("Server listening on port", port)

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print("Connected with client socket", client_socket.fileno())
                
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    message = data.decode()
                    print(f"Client socket {client_socket.fileno()} sent message:", message)

                    reversed_message = message[::-1]
                    client_socket.sendall(reversed_message.encode())
                    print("Sending reply:", reversed_message)

if __name__ == "_main_":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server1.py <port>")
    else:
        main(int(sys.argv[1]))
