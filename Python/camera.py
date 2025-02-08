from flask import Flask, Response
import cv2
import numpy as np
import threading
from ultralytics import YOLO

# Flask app
app = Flask(__name__)

# Global variables for the combined frame and threading lock
combined_frame = None
lock = threading.Lock()

# Load YOLO model
yolo_model = YOLO('/home/pi/Documents/Escendo/yolo_models/ball_model.pt')

def initialize_camera(camera_index, width=320, height=240, fps=30):
    """Initialize a USB camera with specific settings."""
    cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    if not cap.isOpened():
        print(f"Camera {camera_index} could not be opened.")
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    return cap

def apply_yolo(frame):
    """Apply YOLO detection and draw bounding boxes on the frame."""
    results = yolo_model.predict(frame, verbose=False)  # Perform detection
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            confidence = float(box.conf)  # Convert to float
            label = f"{yolo_model.names[int(box.cls)]} {confidence:.2f}"  # Class label

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
    return frame

def capture_frames():
    """Capture frames from two cameras and combine them side by side."""
    global combined_frame
    cam1 = initialize_camera(0)  # Replace with your first camera index
    cam2 = initialize_camera(2)  # Replace with your second camera index

    if cam1 is None or cam2 is None:
        print("One or both cameras could not be initialized. Exiting...")
        return

    try:
        while True:
            # Read frames from both cameras
            ret1, frame1 = cam1.read()
            ret2, frame2 = cam2.read()

            # Handle cases where frames cannot be read
            if not ret1:
                frame1 = np.zeros((240, 320, 3), dtype=np.uint8)  # Black frame for missing camera 1
                cv2.putText(frame1, "Camera 1 Not Available", (50, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            if not ret2:
                frame2 = np.zeros((240, 320, 3), dtype=np.uint8)  # Black frame for missing camera 2
                cv2.putText(frame2, "Camera 2 Not Available", (50, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            # Apply YOLO only to the first camera's frame
            if ret1:
                frame1 = apply_yolo(frame1)

            # Combine frames horizontally
            with lock:
                combined_frame = np.hstack((frame1, frame2))

    except Exception as e:
        print(f"Error in capture_frames: {e}")
    finally:
        cam1.release()
        cam2.release()

def generate_mjpeg():
    """Generate MJPEG stream for Flask."""
    global combined_frame
    while True:
        with lock:
            if combined_frame is None:
                continue
            # Encode the combined frame as JPEG with compression
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # Set JPEG quality to 50
            _, buffer = cv2.imencode('.jpg', combined_frame, encode_param)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/stream')
def stream():
    """Flask route for MJPEG video streaming."""
    return Response(generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Start the capture thread
    capture_thread = threading.Thread(target=capture_frames, daemon=True)
    capture_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=8080)
