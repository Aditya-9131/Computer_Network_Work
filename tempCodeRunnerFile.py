# client_lost_ack.py
import socket
import struct
import random

PORT = 12345
FRAME_SIZE = 256

def receive_frame(sock):
    frame_data = sock.recv(FRAME_SIZE + 4)
    frame_number, data = struct.unpack('I', frame_data[:4])[0], frame_data[4:]
    return frame_number, data

def send_ack(sock, ack_number):
    ack_data = struct.pack('I', ack_number)
    sock.sendall(ack_data)
    print(f"Sent ACK for frame {ack_number}")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', PORT))
    print("Connected to server")

    while True:
        try:
            frame_number, data = receive_frame(client_socket)
            if not data:
                break
            print(f"Received frame {frame_number}: {data.decode()}")
            
            # Simulate lost ACK by skipping ACK for frame number 2
            if frame_number != 2:
                send_ack(client_socket, frame_number)
            else:
                print(f"Simulated loss of ACK for frame {frame_number}")
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
