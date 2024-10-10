from flask import Flask
import cv2

# Function to capture video frames
def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 for webcam, or you can use RTSP/IP Camera URLs
    while True:
        success, frame = cap.read()  # Capture frame-by-frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Concatenate frame one by one and show result
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

