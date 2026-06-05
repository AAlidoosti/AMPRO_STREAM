import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# ====== CHANGE THIS TO ANY WEBPAGE URL YOU WANT ======
TARGET_URL = "https://wttr.in/Manila?png"  # Clean, text-based weather image for testing

@app.route('/shot.jpg')
def single_frame():
    try:
        # We use a free, public screenshot API to convert the webpage to an image cleanly
        # This prevents Render from crashing due to high memory usage
        api_url = f"https://image.thum.io/get/width/320/crop/600/maxAge/1/{TARGET_URL}"
        
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            return Response(response.content, mimetype='image/jpeg')
        else:
            return f"API Error: {response.status_code}", 500
            
    except Exception as e:
        return f"Server Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
