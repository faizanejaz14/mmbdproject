import cv2
from flask import Flask, render_template, Response
import time

video = cv2.VideoCapture(0)
time.sleep(2)
video.set(3, 640)  # Set width to 640 pixels
video.set(4, 480)  # Set height to 480 pixels
app = Flask(__name__)


def video_stream():
    fps_start_time = time.time()
    fps_counter = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()

            # Calculate FPS
            fps_counter += 1
            elapsed_time = time.time() - fps_start_time
            if elapsed_time >= 1.0:  # Update FPS every 1 second
                fps = fps_counter / elapsed_time
                fps_start_time = time.time()
                fps_counter = 0
                print(f"FPS: {fps}")

            yield (b' --frame\r\n'
                   b'Content-type: imgae/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=False)
