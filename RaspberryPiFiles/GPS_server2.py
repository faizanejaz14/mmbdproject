from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import serial
import pynmea2
import re
import mpu_driver as driver

# Making a Flask server to communicate with JS
app = Flask(__name__)
CORS(app)


def parse_direction(direction):
    match = re.match(
        r'(east|west|north|south|left|right),\s*([\d.]+)\s*(km|m)', direction, re.I)
    if match:
        action = match.group(1).lower()
        value = float(match.group(2))
        unit = match.group(3).lower() if match.group(3) else 'm'
        # Convert distance to meters if the unit is in kilometers
        if unit == 'km':
            value *= 1000
        return action, value
    else:
        raise ValueError("Invalid direction format: {}".format(direction))


@app.route('/data', methods=['POST'])
def receive_data_from_JS():
    global Directions
    direction_val = request.json
    print(direction_val)
    if direction_val != "" or direction_val != Directions:
        Directions = direction_val
        parts = Directions.split('\n')
        for i in parts:
            if i == "":
                continue
            action, value = parse_direction(i)
            print(action, " = ", value)
            driver.run_driver(action, value)

        response_data = {"message": Directions}
        return jsonify(response_data)
# function end


@app.route('/sendDataToJS', methods=['GET'])
def send_data_to_JS():
    GPS_reading()
    if Current is None:
        data = ""
    else:
        data = Current
    # Data to send from Python to JavaScript
    return jsonify(data)
# function end


def GPS_reading():
    global Current
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    # converting byte string into string
    newdata = ser.readline().decode("utf-8", errors="ignore")
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        Current = str(round(lat, 6)) + "," + str(round(lng, 6))
    # Temp to send data
    else:
        Current = "0000, 0000"
# function end


def main():
    driver.calibrate_timer()
    # Running Flask Server
    app.run(host='0.0.0.0', port='5000', debug=False)


if __name__ == "__main__":
    main()
