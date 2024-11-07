import os

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


def format_gesture_result(result):
    os.system("cls" if os.name == "nt" else "clear")
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
