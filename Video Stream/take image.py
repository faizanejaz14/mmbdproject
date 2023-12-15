import time
import cv2


def create_webcam_video(output_path='captured_video.mp4', duration=5):
    # Open the webcam (index 0 usually corresponds to the default webcam)
    webcam = cv2.VideoCapture(1)
    time.sleep(2)

    # Check if the webcam is opened successfully
    if not webcam.isOpened():
        print("Error: Could not open webcam.")
        return

    # Set video parameters (adjust as needed)
    frame_width = int(webcam.get(3))  # Width of the frames in the video
    frame_height = int(webcam.get(4))  # Height of the frames in the video
    fps = 30                          # Frames per second

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change the codec as needed
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))

    # Capture frames and write to video file
    start_time = cv2.getTickCount()
    while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
        ret, frame = webcam.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Could not capture frame.")
            break

        # Write the frame to the video file
        out.write(frame)

        # Display the frame (optional)
        cv2.imshow('Webcam Video', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
            break

    # Release the webcam and video writer
    webcam.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video created and saved as {output_path}")


if __name__ == "__main__":
    # Replace 'path/to/your/captured_video.mp4' with the desired output path and filename
    video_path = '/home/Zuck/Desktop/video.mp4'
    create_webcam_video(video_path, duration=5)
