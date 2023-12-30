import socket
import threading
import json
import random
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

#Making a Flask server to communicate with JS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
Current = ""
Directions = ""

@app.route('/data', methods=['POST'])
def receive_data_from_JS():
    global Directions
    direction_val = request.json  # Receive data sent from JavaScript
    if direction_val != "":
        Directions = direction_val
    print("Data received:", Directions)
    # Process the data as needed

    # Send a response back to JavaScript
    response_data = {"message": Directions}
    return jsonify(response_data)

#for python to communicate with raspberryPi
REMOTEIT_URL = 'tcp://proxy60.rt3.io:33444'

def send_data_to_PI(client_socket):
    global Directions
    app.run(debug=True, port=4050) #starting Flask server to update data whenever new data recieved
    old_directions = ""
    try:
        while True:
            try:
                # Read the value from the file "direction.txt"
                #D = "Random" + random()%100
                if old_directions == Directions:
                    continue
                time.sleep(10)
                old_directions = Directions
                client_socket.sendall(json.dumps(Directions).encode())
            except ValueError:
                print("Invalid input")
    except KeyboardInterrupt:
        print("Client interrupted by user")
    finally:
        client_socket.close()


def receive_data_from_GPS(client_socket):
    # Example usage:
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
    #Running Flask Server
    parts = REMOTEIT_URL.split(':')
    host = parts[1][2:]
    port = int(parts[2])
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        client_thread1 = threading.Thread(target=send_data_to_PI, args=(client_socket,))
        client_thread2 = threading.Thread(
            target=receive_data_from_GPS, args=(client_socket,))
        client_thread1.start()
        client_thread2.start()
        client_thread1.join()
        client_thread2.join()
    except:
        print("No connection to raspberry Pi")

if __name__ == "__main__":
    main()
