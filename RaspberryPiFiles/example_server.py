import socket
import threading
import time
import json
import random

Current = {"latitude": 0.0, "longitude": 0.0}
Destination = {"latitude": 0.0, "longitude": 0.0}


def send_data(client_socket, client_address):
    try:
        while True:
            global Current
            Current = {
                "latitude": round(random.uniform(33.623615, 33.619145), 6),
                "longitude": round(random.uniform(72.959337, 72.956741), 6),
            }
            print(f"Current coordinates created: {Current}")
            time.sleep(10)
            client_socket.sendall(json.dumps(Current).encode())
    except (socket.error, KeyboardInterrupt):
        print(f"Connection with {client_address} closed")
    finally:
        client_socket.close()


def recieve_data(client_socket, client_address):
    global Destination
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection with {client_address} closed")
                break
            new_destination = json.loads(data.decode())
            if Destination != new_destination:
                Destination = new_destination
                print(f"Destination changed: {Destination}")
            else:
                print(f"Destination unchanged: {Destination}")
    except (socket.error, KeyboardInterrupt):
        print(f"Connection with {client_address} closed")
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5001))
    server_socket.listen()
    print("Server listening on port 5001")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            # Create separate threads for each client
            client_thread1 = threading.Thread(
                target=send_data, args=(client_socket, client_address))
            client_thread2 = threading.Thread(
                target=recieve_data, args=(client_socket, client_address))

            # Start both threads
            client_thread1.start()
            client_thread2.start()

            # Wait for both threads to finish
            client_thread1.join()
            client_thread2.join()
    except KeyboardInterrupt:
        print("Server interrupted by user")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
