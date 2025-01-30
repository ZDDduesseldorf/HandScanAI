import time
from fastapi.websockets import WebSocketState
from app.core.config import settings
from app.db.models import ScanEntry
from lib.opencv.sharpness import calculate_sharpness
import numpy as np
import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid
import os

ws_router = APIRouter()


@ws_router.websocket("/{id}")
async def webcam_flow(websocket: WebSocket, id: str):
    """
    WebSocket endpoint for the webcam flow

    The id of the ScanEntry must be provided in the URL.

    URL-Scheme like this following 'ws://localhost:8000/ws/${id}'

    Flows:
    - error:
        {
            "flow": "error",
            "message": str  # Error message
        }
    - validation:
        {
            "flow": "validation",
            "landmarks_detected": bool,
            "hand_is_spread": bool,
            "hand_is_visible": bool
        }
    - timer:
        {
            "flow": "timer",
            "time": int  # Time remaining in seconds
        }
    - taking_images:
        {
            "flow": "taking_images"
        }
    - success:
        {
            "flow": "success",
            "image": str  # URL to the saved image
        }
    """

    # Accept the websocket connection
    await websocket.accept()

    # Check if entry model doesn't exist or is confirmed
    scan_entry_model = await ScanEntry.get(id)
    if scan_entry_model is None or scan_entry_model.confirmed:
        message = (
            f"ScanEntry with id {id} not found"
            if scan_entry_model is None
            else f"ScanEntry with id {id} is already confirmed and cannot be modified"
        )
        await websocket.send_json({"flow": "error", "message": message})
        await websocket.close()
        return

    # Initialize variables
    start_time = None
    wait_time = 3
    photos_to_take = 3
    images = []

    try:
        # Continuously receive images from the client
        while websocket.client_state == WebSocketState.CONNECTED:
            # Receive the image from the client
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                await websocket.send_json(
                    {
                        "flow": "error",
                        "message": "failed to decode image",
                    }
                )
                continue

            validation_pipeline_result = validation_pipeline(image)

            if is_validation_pipeline_valid(validation_pipeline_result):
                current_time = time.time()
                # Start the timer
                if start_time is None:
                    await websocket.send_json(
                        {
                            "flow": "timer",
                            "time": wait_time,
                        }
                    )
                    start_time = current_time
                # Countdown
                elif current_time - start_time < wait_time:
                    await websocket.send_json(
                        {
                            "flow": "timer",
                            "time": wait_time - int(current_time - start_time),
                        }
                    )
                # Start taking images
                elif current_time - start_time >= wait_time:
                    await websocket.send_json(
                        {
                            "flow": "taking_images",
                        }
                    )
                    if len(images) < photos_to_take:
                        images.append(image)
                    else:
                        # Find the sharpest image
                        sharpest_image = max(images, key=calculate_sharpness)
                        save_path = os.path.join(settings.PATHS.MEDIA_DIR, "QueryImages", f"{id}.jpg")
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        cv2.imwrite(save_path, sharpest_image)
                        await websocket.send_json(
                            {
                                "flow": "success",
                                "image": f"{settings.SERVER_HOST}rest/image?image_id={id}",
                            }
                        )
                        await websocket.close()
                        return
            else:
                # Reset the variables
                start_time = None
                images = []

                await websocket.send_json(
                    {
                        "flow": "validation",
                        "landmarks_detected": validation_pipeline_result["landmarks_detected"],
                        "hand_is_spread": validation_pipeline_result["hand_is_spread"],
                        "hand_is_visible": validation_pipeline_result["hand_is_visible"],
                    }
                )

    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        print("Closing websocket connection")
