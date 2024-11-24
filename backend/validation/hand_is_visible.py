def hand_is_visible(landmarks, image_dimensions):
    """Checks if the hand is visible in the image"""

    if landmarks is None:
        return False

    if len(landmarks) != 21:
        return False

    # All landmarks should be visible inside the image
    for landmark in landmarks:
        x, y = landmark
        if x < 0 or x >= image_dimensions[1] or y < 0 or y >= image_dimensions[0]:
            return False

    return True
