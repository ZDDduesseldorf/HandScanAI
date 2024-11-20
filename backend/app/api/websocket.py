import numpy as np
import cv2
from fastapi import WebSocket, WebSocketDisconnect
from lib.mediapipe import draw, recognizer, utils
from app.core.config import settings

from ..validation.spread_check import spread_check

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Accepted websocket connection")
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                print("Failed to decode image")
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            gesture_recognition_result = recognizer.recognize_gesture(image)

            # Print the human-readable result        
            #print(utils.format_gesture_result(gesture_recognition_result))
            

            if gesture_recognition_result.hand_landmarks:
                image_height, image_width, _ = image.shape
                landmarks = [
                    (int(l.x * image_width), int(l.y * image_height))
                    for l in gesture_recognition_result.hand_landmarks[0]
                ]
                image = draw.draw_landmarks(image, landmarks)

                print(spread_check(landmarks))

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode(".jpg", image)
            await websocket.send_bytes(buffer.tobytes())
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        print("Closing websocket connection")