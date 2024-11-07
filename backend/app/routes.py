import os

import cv2
import numpy as np
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from app.core.config import settings
from lib.mediapipe import draw, recognizer, utils

router = APIRouter()


@router.get("/")
async def get():
    file = os.path.join(settings.PATHS.STATIC_DIR, "index.html")
    if not os.path.exists(file):
        return {"error": "File not found"}
    return FileResponse(file)


@router.websocket("/ws")
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
            print(utils.format_gesture_result(gesture_recognition_result))

            if gesture_recognition_result.hand_landmarks:
                image_height, image_width, _ = image.shape
                landmarks = [
                    (int(l.x * image_width), int(l.y * image_height))
                    for l in gesture_recognition_result.hand_landmarks[0]
                ]
                image = draw.draw_landmarks(image, landmarks)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode(".jpg", image)
            await websocket.send_bytes(buffer.tobytes())
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        print("Closing websocket connection")
