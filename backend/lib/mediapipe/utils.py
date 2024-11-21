from lib.mediapipe import recognizer
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

def format_gesture_recognizer_result(result):
    if not result.gestures or not result.handedness or not result.hand_landmarks:
        return "Nothing detected"
    gesture = result.gestures[0][0]
    handedness = result.handedness[0][0]
    landmarks = result.hand_landmarks[0]
    gesture_info = (
        f"Detected Gesture:\n"
        f"  - Name: {gesture.category_name}\n"
        f"  - Confidence Score: {gesture.score:.2%}\n\n"
        f"Handedness:\n"
        f"  - Hand: {handedness.category_name}\n"
        f"  - Confidence Score: {handedness.score:.2%}\n\n"
        f"Normalized Landmarks:\n"
    )
    for i, landmark in enumerate(landmarks):
        gesture_info += f"  - {LANDMARK_NAMES[i]}: (x: {landmark.x:.4f}, y: {landmark.y:.4f}, z: {landmark.z:.4f})\n"
    return gesture_info

def extract_landmarks_from_gesture_recognizer(image):
    gesture_recognition_result = recognizer.recognize_gesture(image)
    if gesture_recognition_result.hand_landmarks:
        image_height, image_width, _ = image.shape
        landmarks = [
            (int(l.x * image_width), int(l.y * image_height))
            for l in gesture_recognition_result.hand_landmarks[0]
        ]
        return landmarks
    return None

def extract_landmarks(image):
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5
    ) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            image_height, image_width, _ = image.shape
            landmarks = [
                (int(l.x * image_width), int(l.y * image_height))
                for l in results.multi_hand_landmarks[0].landmark
            ]
            return landmarks
    return None