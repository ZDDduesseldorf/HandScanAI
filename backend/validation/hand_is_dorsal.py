from hand_normalization.src.main import calculate_hand_orientation

def hand_is_dorsal(landmarks: list, handedness: str)-> bool: 
    """
    Check if the dorsal side of the hand is pointed towards the camera.

    :param landmarks: List of landmarks of the hand (as returned by MediaPipe or similar library).
    :param handedness: string thats "Left" or "Right"
    :return: True the dorsal side of the hand is pointed towards the camera, False otherwise.
    """
    hand_orientation = calculate_hand_orientation(landmarks)

    if (handedness == "Right") and (hand_orientation == 0):
        return True
    if (handedness == "Left") and (hand_orientation == 1):
        return True
    else:
        return False
    
