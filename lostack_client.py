import socket
import struct

PORT = 12345
FRAME_SIZE = 10  

def receive_frame(sock):
    try:
        
        buffer = b''
        while len(buffer) < FRAME_SIZE + 4:
            part = sock.recv(FRAME_SIZE + 4 - len(buffer))
            if not part:
                raise ValueError("Connection closed by the server")
            buffer += part

        if len(buffer) < 4:
            raise ValueError("Received incomplete frame header")

        frame_number, data = struct.unpack('I', buffer[:4])[0], buffer[4:]
        return frame_number, data

    except Exception as e:
        print(f"Error receiving frame: {e}")
        return None, None

def send_ack(sock, ack_number):
    ack_data = struct.pack('I', ack_number)
    try:
        sock.sendall(ack_data)
        print(f"Sent ACK for frame {ack_number}")
    except Exception as e:
        print(f"Error sending ACK: {e}")

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', PORT))
        print("Connected to server")
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    while True:
        try:
            frame_number, data = receive_frame(client_socket)
            if frame_number is None:
                break
            if not data:
                print("No data received, ending connection.")
                break
            data_size = len(data)
            print(f"Received frame {frame_number}: {data_size} bytes | Data: {data.decode(errors='ignore').strip()}")
            
            
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
