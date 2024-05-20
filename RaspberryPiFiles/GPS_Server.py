import socket
import threading
import time
import json
import serial
import pynmea2

Current = ""
Destination = ""


def send_data(client_socket, client_address):
    try:
        while True:
            GPS_reading()
            client_socket.sendall(json.dumps(Current).encode())
            time.sleep(5)
    except (socket.error, KeyboardInterrupt):
        print(f"Connection with {client_address} closed")
    finally:
        client_socket.close()
#   function end


def GPS_reading():
    global Current
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    # converting byte string into string
    newdata = ser.readline().decode("windows-1252")
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        Current = str(round(lat, 6)) + "," + str(round(lng, 6))


def recieve_data(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection with {client_address} closed")
                break
            global Destination
            Destination = data.decode()
            print(f"Destination: {Destination}")
    except (socket.error, KeyboardInterrupt):
        print(f"Connection with {client_address} closed")
    finally:
        client_socket.close()
#   function end


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5000
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen()
    print(f"Server listening on port: {port}")

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
