

def hand_is_dorsal(landmarks: list, handedness: str)-> bool: 
    """
    Check if the dorsal side of the hand is pointed towards the camera.

    :param landmarks: List of landmarks of the hand (as returned by MediaPipe or similar library).
    :param handedness: string thats "Left" or "Right"
    :return: True the dorsal side of the hand is pointed towards the camera, False otherwise.
    """
    hand_orientation = calculate_thumb_position(landmarks)
    
    if (handedness == "Right") and (hand_orientation == 0):
        return True
    if (handedness == "Left") and (hand_orientation == 1):
        return True
    else:
        return False
    
def calculate_thumb_position(landmarks: list) -> int:
    """
    Determines the hand orientation based on landmarks.

    Args:
        landmarks (list): List of hand landmarks, where each landmark is a tuple (x, y).

    Returns:
        int: Orientation of the hand. Returns 1 for dorsal righthand and palmal lefthand. 0 otherwise.
    """
    ring_finger_base = landmarks[13]
    index_finger_base = landmarks[5]
    base = landmarks[0]

    if abs(ring_finger_base[0] - index_finger_base[0]) > abs(ring_finger_base[1] - index_finger_base[1]):
        if ring_finger_base[0] > index_finger_base[0]:
            if base[1] > index_finger_base[1]:
                return 1
            else:
                return 0
        else:
            if base[1] < index_finger_base[1]:
                return 1
            else:
                return 0
    else:
        if ring_finger_base[1] < index_finger_base[1]:
            if base[0] > index_finger_base[0]:
                return 1
            else:
                return 0
        else:
            if base[0] < index_finger_base[0]:
                return 1
            else:
                return 0