import socket
import struct

PORT = 12345
FRAME_SIZE = 10  

def receive_frame(sock):

    header = b''
    while len(header) < 4:
        part = sock.recv(4 - len(header))
        if not part:
            raise ValueError("Connection closed by the server")
        header += part

    
    frame_number = struct.unpack('I', header)[0]

    
    remaining_data = FRAME_SIZE
    data = b''
    while remaining_data > 0:
        part = sock.recv(remaining_data)
        if not part:
            raise ValueError("Connection closed by the server")
        data += part
        remaining_data -= len(part)
    
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
            if data == b'':
                break
            data_size = len(data)
            print(f"Received frame {frame_number}: {data_size} bytes | Data: {data.decode(errors='ignore').strip()}")
            send_ack(client_socket, frame_number)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
