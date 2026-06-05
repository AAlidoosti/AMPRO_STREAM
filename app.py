import cv2
import os
import glob
from flask import Flask, Response

app = Flask(__name__)

# Global variables to track position in the playlist
video_playlist = []
current_video_idx = 0
cap = None

def update_playlist():
    global video_playlist
    # Dynamically scan the directory for all .mp4 files
    video_playlist = sorted(glob.glob("*.mp4"))
    print(f"Current Playlist updated: {video_playlist}")

@app.route('/shot.jpg')
def single_frame():
    global video_playlist, current_video_idx, cap
    
    # 1. Update playlist dynamically on the fly
    update_playlist()
    
    if not video_playlist:
        return "No MP4 files found in directory", 404
        
    # 2. Initialize the video capture if not already running
    if cap == None:
        if current_video_idx >= len(video_playlist):
            current_video_idx = 0
        cap = cv2.VideoCapture(video_playlist[current_video_idx])
        print(f"Playing video: {video_playlist[current_video_idx]}")

    # 3. Read the next sequential frame
    success, frame = cap.read()
    
    # 4. If a video ends, move to the next file automatically
    if not success:
        cap.release()
        current_video_idx = (current_video_idx + 1) % len(video_playlist)
        cap = cv2.VideoCapture(video_playlist[current_video_idx])
        print(f"Moving to next video: {video_playlist[current_video_idx]}")
        success, frame = cap.read()

    if success:
        # Downscale and compress for the ESP32-S3 LCD
        frame = cv2.resize(frame, (320, 240))
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 55])
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    
    return "Error reading frame", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
