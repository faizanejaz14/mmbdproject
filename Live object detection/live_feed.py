import cv2
import numpy as np
import requests
from io import BytesIO

# Load the pre-trained MobileNet SSD model
net = cv2.dnn.readNetFromTensorflow(
    r'F:\Navigation\ssd_mobilenet_v1_coco_2018_01_28\frozen_inference_graph.pb',
    r'F:\Navigation\ssd_mobilenet_v1_coco_2018_01_28\ssd_mobilenet_v1_coco.pbtxt'
)


# URL for the video stream
video_url = 'http://192.168.43.132:5000'  # Replace with your actual URL

# Open the video stream
stream = requests.get(video_url, stream=True)
stream.raise_for_status()

# Function to decode and preprocess image


def preprocess_image(image):
    image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    image = cv2.resize(image, (300, 300))
    return image

# Function to perform object detection on an image


def detect_objects(image):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Adjust confidence threshold as needed
            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * \
                np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw bounding box and label on the image
            cv2.rectangle(image, (startX, startY),
                          (endX, endY), (0, 255, 0), 2)
            label = f"Class: {class_id}, Confidence: {confidence:.2f}"
            cv2.putText(image, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image


# Open a video stream
cap = cv2.VideoCapture()

# Read frames from the video stream
while True:
    try:
        # Get the next frame from the video stream
        frame = next(stream.iter_content(chunk_size=4096))
        frame = preprocess_image(frame)
        frame = detect_objects(frame)

        # Display the frame with detected objects
        cv2.imshow('Object Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e}")

# Release the video stream and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
