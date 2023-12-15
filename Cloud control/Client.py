import socket
import threading
import json
import random
import time

REMOTEIT_URL = 'tcp://proxy61.rt3.io:36072'
Current = ""
Destination = 0.0


def send_data(client_socket):
    try:
        while True:
            try:
                global Destination
                Destination = round(random.uniform(0.0, 100.0), 6)
                time.sleep(10)
                client_socket.sendall(json.dumps(Destination).encode())
            except ValueError:
                print("Invalid input")
    except KeyboardInterrupt:
        print("Client interrupted by user")
    finally:
        client_socket.close()


def receive_data(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            global Current
            Current = data.decode()
            print(f"Current: {Current}")
    except KeyboardInterrupt:
        print("Client interrupted by user")
    finally:
        client_socket.close()


def main():
    parts = REMOTEIT_URL.split(':')
    host = parts[1][2:]
    port = int(parts[2])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_thread1 = threading.Thread(target=send_data, args=(client_socket,))
    client_thread2 = threading.Thread(
        target=receive_data, args=(client_socket,))
    client_thread1.start()
    client_thread2.start()
    client_thread1.join()
    client_thread2.join()


if __name__ == "__main__":
    main()
