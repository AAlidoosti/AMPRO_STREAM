import os
from flask import Flask, Response
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# ====== CHANGE THIS TO ANY WEBPAGE YOU WANT TO SHOW ======
TARGET_URL = "https://weather.com" 

@app.route('/shot.jpg')
def single_frame():
    try:
        with sync_playwright() as p:
            # Launch a invisible cloud browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set the browser window size to perfectly match or scale to your LCD aspect ratio
            page.set_viewport_size({"width": 640, "height": 480})
            
            # Load the webpage
            page.goto(TARGET_URL, wait_until="networkidle")
            
            # Take a crisp snapshot directly into memory (High Quality = 90)
            img_bytes = page.screenshot(type="jpeg", quality=90, scale="css")
            browser.close()
            
            return Response(img_bytes, mimetype='image/jpeg')
    except Exception as e:
        return f"Error capturing webpage: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
