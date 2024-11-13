import numpy as np
import cv2
from fastapi import WebSocket, WebSocketDisconnect
from lib.mediapipe import draw, recognizer, utils
from app.core.config import settings
from itertools import combinations

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
            
            #define indices of finger joints 
            #source: mediapipe api docs:
            #https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer
            finger_indices = {
                "thumb": 3,
                "index": 6,
                "middle": 10,
                "ring": 14,
                "pinky": 18,
            }

            if gesture_recognition_result.hand_landmarks:
                image_height, image_width, _ = image.shape
                landmarks = [
                    (int(l.x * image_width), int(l.y * image_height))
                    for l in gesture_recognition_result.hand_landmarks[0]
                ]
                image = draw.draw_landmarks(image, landmarks)

                #get coordinates for each finger joint
                fingers = {name: landmarks[idx] for name, idx in finger_indices.items()}

                #define the order of adjacent fingers
                adjacent_fingers = ["thumb", "index", "middle", "ring", "pinky"]

                #calculate distance of adjacent fingers 
                #adjacent fingers are relevant for measuring spread
                adjacent_distances = {}
                for i in range(len(adjacent_fingers) - 1):
                    finger1 = adjacent_fingers[i]
                    finger2 = adjacent_fingers[i + 1]
                    
                    coord1 = fingers[finger1]
                    coord2 = fingers[finger2]
                    
                    #calculate euclidian distance (in pixels)
                    distance = np.linalg.norm(np.array(coord1) - np.array(coord2))
                    adjacent_distances[(finger1, finger2)] = distance

                #for now just print the distance to the console
                for finger_pair, distance in adjacent_distances.items():
                    print(f"Distance between {finger_pair[0]} and {finger_pair[1]}: {distance:.2f} pixels")
                    #todo: define threshold and return boolean if spread is ok

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode(".jpg", image)
            await websocket.send_bytes(buffer.tobytes())
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        print("Closing websocket connection")