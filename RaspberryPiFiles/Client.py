import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import re
import random

app = Flask(__name__)
CORS(app)  # , resources={r"/data": {"origins": "http://127.0.0.1:5501"}})

Current = ""
Directions = ""


def parse_direction(direction):
    match = re.match(
        r'(east|west|north|south|left|right|U-turn),\s*([\d.]+)\s*(km|m)', direction, re.I)
    if match:
        action = match.group(1).lower()
        value = float(match.group(2))
        unit = match.group(3).lower() if match.group(3) else 'm'
        if unit == 'km':
            value *= 1000
        return action, value
    else:
        raise ValueError("Invalid direction format: {}".format(direction))


def drive_motors():
    print()


@app.route('/data', methods=['POST'])
def receive_data_from_JS():
    global Directions
    direction_val = request.json
    if direction_val != "" or direction_val != Directions:
        Directions = direction_val
        parts = Directions.split('\n')
        for i in parts:
            if i == "":
                continue
            action, value = parse_direction(i)
            print(action, " = ", value)

        response_data = {"message": Directions}
        return jsonify(response_data)


@app.route('/sendDataToJS', methods=['GET'])
def send_data_to_JS():
    Current = [round(random.uniform(79, 80), 6),
            round(random.uniform(79, 80), 6)]
    time.sleep(1.5)
    response_data = {"message": f'Latitude: {Current[0]}\nLongitude: {Current[1]}'}
    print(response_data)
    return jsonify(response_data)


def main():
    app.run(host='0.0.0.0', port='5000', debug=False)


if __name__ == "__main__":
    main()