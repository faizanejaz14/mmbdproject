import socket
import threading
import json
import random
import time

REMOTEIT_URL = 'tcp://proxy60.rt3.io:33444'
Current = ""
Destination = 0.0

def overwrite_file(file_path, new_data):
    try:
        # Read the current content of the file
        with open(file_path, 'r') as file:
            current_data = file.read()

        # Compare the current content with the new data
        if current_data != new_data:
            # Write the new data to the file (overwriting the existing content)
            with open(file_path, 'w') as file:
                file.write(new_data)
                print("File overwritten successfully with new data.")
        else:
            print("New data is the same as the existing content. File not overwritten.")

    except FileNotFoundError:
        # If the file doesn't exist, create it and write the new data
        with open(file_path, 'w') as file:
            file.write(new_data)
            print("File created and written with new data.")

def read_direction_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found")
        return None
    except ValueError:
        print("Invalid content in file")
        return None

def send_data(client_socket):
    try:
        while True:
            try:
                global Destination
                # Read the value from the file "direction.txt"
                direction_value = read_direction_from_file("../direction.txt")
                if direction_value is None:
                    Destination = "EMPTTYYT"
                else:
                    Destination = direction_value
                time.sleep(10)
                client_socket.sendall(json.dumps(Destination).encode())
            except ValueError:
                print("Invalid input")
    except KeyboardInterrupt:
        print("Client interrupted by user")
    finally:
        client_socket.close()


def receive_data(client_socket):
    # Example usage:
    file_path = '../GPS_Data.txt'  # File path to save the value
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            global Current
            Current = data.decode()

            print(f"Current: {Current}")
            overwrite_file(file_path, Current)
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
