import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

LANDMARK_NAMES = [
    "WRIST",
    "THUMB_CMC",
    "THUMB_MCP",
    "THUMB_IP",
    "THUMB_TIP",
    "INDEX_FINGER_MCP",
    "INDEX_FINGER_PIP",
    "INDEX_FINGER_DIP",
    "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP",
    "MIDDLE_FINGER_PIP",
    "MIDDLE_FINGER_DIP",
    "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP",
    "RING_FINGER_PIP",
    "RING_FINGER_DIP",
    "RING_FINGER_TIP",
    "PINKY_MCP",
    "PINKY_PIP",
    "PINKY_DIP",
    "PINKY_TIP",
]


def extract_landmarks(image):
    """Extracts landmarks from an image"""

    with mp_hands.Hands(
        max_num_hands=1,
        min_tracking_confidence=0.6,
        min_detection_confidence=0.6,
        model_complexity=1,
    ) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            image_height, image_width, _ = image.shape
            landmarks = [
                (int(landmark.x * image_width), int(landmark.y * image_height))
                for landmark in results.multi_hand_landmarks[0].landmark
            ]
            return landmarks
    return None
