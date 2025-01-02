import socket
import threading
import time
import struct

PORT = 12345
FRAME_SIZE = 10  
TIMEOUT_SEC = 2
TOTAL_FRAMES = 5
FILE_PATH = 'lab4\data.txt'  

class TimerThread(threading.Thread):
    def __init__(self, timer_event):
        super().__init__()
        self.timer_event = timer_event

    def run(self):
        while True:
            time.sleep(TIMEOUT_SEC)
            if self.timer_event.is_set():
                self.timer_event.clear()
                print("Timer expired. Resending frame.")

def send_frame(sock, frame_number, data):
    frame = struct.pack('I', frame_number) + data
    sock.sendall(frame)
    data_size = len(data)
    print(f"Sent frame {frame_number}: {data_size} bytes | Data: {data.decode(errors='ignore')}")

def receive_ack(sock):
    ack_data = sock.recv(4)
    if len(ack_data) < 4:
        raise ValueError("Received incomplete ACK")
    ack_number = struct.unpack('I', ack_data)[0]
    print(f"Received ACK for frame {ack_number}")

def main():
    timer_event = threading.Event()
    timer_thread = TimerThread(timer_event)
    timer_thread.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1)
    print("Server is listening...")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    with open(FILE_PATH, 'rb') as file:  
        for frame_number in range(1, TOTAL_FRAMES + 1):
            data = file.read(FRAME_SIZE)  
            if not data:  
                break
            data = data.ljust(FRAME_SIZE, b'\x00')  
            send_frame(conn, frame_number, data)
            timer_event.set()

            try:
                conn.settimeout(TIMEOUT_SEC)
                receive_ack(conn)
                timer_event.clear()  
            except socket.timeout:
                print("Timeout occurred. Resending frame...")
                timer_event.set()

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()
