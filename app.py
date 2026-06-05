import cv2
import os
from flask import Flask, Response

app = Flask(__name__)

# Load your video file from the folder
VIDEO_PATH = "video.mp4"

@app.route('/shot.jpg')
def single_frame():
    if not os.path.exists(VIDEO_PATH):
        return "Video file missing", 404
        
    camera = cv2.VideoCapture(VIDEO_PATH)
    success, frame = camera.read()
    camera.release()
    
    if success:
        # Resize to fit your ESP32 LCD precisely
        frame = cv2.resize(frame, (320, 240))
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 55])
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    
    return "Error reading video frame", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)