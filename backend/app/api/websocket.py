import time
from fastapi.websockets import WebSocketState
from app.core.config import settings
from app.utils.uuid import generate_uuid
from lib.mediapipe.utils import extract_landmarks_from_gesture_recognizer
from lib.opencv.sharpness import calculate_sharpness
import numpy as np
import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.validation.spread_check import spread_check
import os

ws_router = APIRouter()

@ws_router.websocket("/")
async def webcam_flow(websocket: WebSocket):
    """ WebSocket endpoint for the webcam flow """
    # Accept the websocket connection
    await websocket.accept()

    # Initialize variables
    start_time = None
    wait_time = 3
    photos_to_take = 20
    images = []

    try:
        # Continuously receive images from the client
        while websocket.client_state == WebSocketState.CONNECTED:
            # Receive the image from the client
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                print("Failed to decode image")
                continue
            
            # Extract landmarks from the image
            landmarks = extract_landmarks_from_gesture_recognizer(image)
            # Check if the hand is spread
            spread_check_data = spread_check(landmarks)

            if spread_check_data:
                current_time = time.time()
                # Start the timer
                if start_time is None:
                    await websocket.send_json({
                        "flow": "timer",
                        "time": wait_time,
                    })
                    start_time = current_time
                # Countdown
                elif current_time - start_time < wait_time:
                    await websocket.send_json({
                        "flow": "timer",
                        "time": wait_time - int(current_time - start_time),
                    })
                # Start taking images
                elif current_time - start_time >= wait_time:
                    await websocket.send_json({
                        "flow": "taking_images",
                    })
                    if len(images) < photos_to_take:
                        images.append(image)
                    else:
                        # Find the sharpest image
                        sharpest_image = max(images, key=calculate_sharpness)
                        uuid = generate_uuid()
                        save_path = os.path.join(settings.PATHS.MEDIA_DIR, "images" ,f"{uuid}.jpg")
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        cv2.imwrite(save_path, sharpest_image)
                        await websocket.send_json({
                            "flow": "success",
                            "image": f"{settings.SERVER_HOST}rest/image?image_id={uuid}",
                        })
                        await websocket.close()
            else:
                # Reset the variables
                start_time = None
                images = []

                await websocket.send_json({
                    "flow": "webcam_checks",
                    "landmarks_detected": landmarks is not None,
                    "spread_check": spread_check_data,
                })

    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        print("Closing websocket connection")