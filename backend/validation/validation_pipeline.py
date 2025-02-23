from lib.mediapipe.utils import extract_landmarks
from validation.hand_is_spread import hand_is_spread
from validation.hand_is_visible import hand_is_visible
from validation.hand_is_dorsal import hand_is_dorsal


def validation_pipeline(image):
    """Runs the validation pipeline for the given image and returns the result for each validation"""

    # Extract landmarks from the image
    landmarks, handedness = extract_landmarks(image)

    # Get the image dimensions
    image_dimensions = image.shape

    # Check if the hand is fully visible
    is_hand_visible = hand_is_visible(landmarks, image_dimensions)

    # Check if the hand is spread
    is_hand_spread = hand_is_spread(landmarks)

    # Check if the hand is dorsal
    is_hand_dorsal = hand_is_dorsal(landmarks,handedness)
    
    return {
        "hand_is_spread": is_hand_spread,
        "landmarks_detected": landmarks is not None,
        "hand_is_visible": is_hand_visible,
        "hand_is_dorsal": is_hand_dorsal,
    }


def is_validation_pipeline_valid(validation_result) -> bool:
    """Checks if the validation pipeline result is valid"""

    return (
        validation_result["hand_is_spread"]
        and validation_result["landmarks_detected"]
        and validation_result["hand_is_visible"]
        and validation_result["hand_is_dorsal"]
    )
