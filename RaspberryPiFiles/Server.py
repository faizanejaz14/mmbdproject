import socket
import threading
import time
import json

Current = 45.123456
Destination = 0.0


def send_data(client_socket, client_address):
    try:
        while True:
            client_socket.sendall(json.dumps(Current).encode())
            time.sleep(5)
    except (socket.error, KeyboardInterrupt):
        print(f"Connection with {client_address} closed")
    finally:
        client_socket.close()
#   function end


def recieve_data(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection with {client_address} closed")
                break
            global Destination
            if Destination != data.decode():
                Destination = data.decode()
                print(f"Destination changed: {Destination}")
            print(f"Destination unchanged: {Destination}")
    except (socket.error, KeyboardInterrupt):
        print(f"Connection with {client_address} closed")
    finally:
        client_socket.close()
#   function end


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5001))
    server_socket.listen()
    print("Server listening on port 5001")

    try:
        client_socket, client_address = server_socket.accept()
        client_thread1 = threading.Thread(
            target=send_data, args=(client_socket, client_address))
        client_thread2 = threading.Thread(
            target=recieve_data, args=(client_socket, client_address))
        client_thread1.start()
        client_thread2.start()
        client_thread1.join()
        client_thread2.join()
    except KeyboardInterrupt:
        print("Server interrupted by user")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
