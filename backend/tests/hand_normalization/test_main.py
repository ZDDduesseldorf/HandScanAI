import pytest
import numpy as np
import cv2
import os
from pathlib import Path
from hand_normalization.src import main

# Run in Terminal with: pytest tests/hand_normalization

# === Global Paths === #
BASE_DIR = Path(__file__).resolve().parent.parent  # /tests
TEST_IMAGE_DIR = BASE_DIR / "data" / "TestImages"


def test_normalize_hand_image(absolute_image_path):
    temp_uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    regions_dict = main.normalize_hand_image(absolute_image_path)
    # expect 7 items in image_tensors
    assert len(regions_dict) == 7


# === FIXTURES === #
@pytest.fixture
def valid_image_path():
    """Provides the path to a valid hand image."""
    return str(TEST_IMAGE_DIR / "Hand_0000002.jpg")


@pytest.fixture
def invalid_image_path():
    """Provides the path to a non-existing image."""
    return str(TEST_IMAGE_DIR / "non_existing.jpg")


@pytest.fixture
def corrupted_image_path(tmp_path):
    """Creates a temporary, corrupted image file."""
    corrupted_file = tmp_path / "corrupted.jpg"
    corrupted_file.write_text("This is not valid image content.")
    return str(corrupted_file)


@pytest.fixture
def empty_image(tmp_path):
    """Creates a blank (empty) image for testing."""
    empty_img_path = tmp_path / "empty.jpg"
    import cv2
    import numpy as np

    blank_image = np.zeros((500, 500, 3), dtype=np.uint8)
    cv2.imwrite(str(empty_img_path), blank_image)
    return str(empty_img_path)


# === TESTS FOR load_image === #
def test_load_valid_image(valid_image_path):
    """Tests loading a valid image file."""
    image = main.load_image(valid_image_path)
    assert isinstance(image, np.ndarray), "The loaded image should be a NumPy array."
    assert image.size > 0, "The image should not be empty."


def test_load_non_existing_image(invalid_image_path):
    """Tests if loading a non-existing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        main.load_image(invalid_image_path)


def test_load_corrupted_image(corrupted_image_path):
    """Tests if loading a corrupted image raises ValueError."""
    with pytest.raises(ValueError):
        main.load_image(corrupted_image_path)


# === TESTS FOR get_landmarks === #
def test_get_landmarks_valid_image(valid_image_path):
    """Tests if landmarks are detected in a valid hand image."""
    landmarks = main.get_landmarks(valid_image_path)
    assert isinstance(landmarks, list), "The result should be a list."
    assert all(isinstance(point, tuple) and len(point) == 2 for point in landmarks), (
        "All landmarks should be (x, y) tuples."
    )
    assert len(landmarks) > 0, "There should be at least one detected landmark."


def test_get_landmarks_no_hand(empty_image):
    """Tests if an image without a hand returns an empty landmark list."""
    landmarks = main.get_landmarks(empty_image)
    assert isinstance(landmarks, list), "The result should be a list."
    assert len(landmarks) == 0, "No landmarks should be detected in a blank image."


def test_get_landmarks_invalid_path(invalid_image_path):
    """Tests if an invalid path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        main.get_landmarks(invalid_image_path)


# === TESTS FOR create_handmask === #
def test_create_handmask_with_skin_color_image():
    """Tests if the hand mask correctly identifies skin-colored regions."""
    # Create a synthetic skin-colored image in BGR format
    skin_bgr = np.full((100, 100, 3), (45, 60, 100), dtype=np.uint8)  # Approximate skin color
    mask = main.create_handmask(skin_bgr)

    # Check if the mask is not empty (should detect skin-colored region)
    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == (100, 100), "The mask should have the same spatial dimensions as the input image."
    assert mask.sum() > 0, "The mask should detect skin-colored areas and not be empty."


def test_create_handmask_with_non_skin_color_image():
    """Tests if the hand mask correctly ignores non-skin-colored regions."""
    # Create a blue image (non-skin color)
    blue_bgr = np.full((100, 100, 3), (255, 0, 0), dtype=np.uint8)  # Pure blue in BGR
    mask = main.create_handmask(blue_bgr)

    # Check if the mask is completely black (no skin detected)
    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == (100, 100), "The mask should have the same spatial dimensions as the input image."
    assert mask.sum() == 0, "The mask should be empty for non-skin-colored regions."


def test_create_handmask_with_empty_image():
    """Tests if the function handles an empty image correctly."""
    empty_image = np.zeros((100, 100, 3), dtype=np.uint8)  # Completely black image
    mask = main.create_handmask(empty_image)

    # Check if the mask is completely black
    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == (100, 100), "The mask should have the same spatial dimensions as the input image."
    assert mask.sum() == 0, "The mask should be empty for a completely black image."


# === TESTS FOR detect_hand_contours === #
def test_detect_hand_contours_with_valid_mask():
    """Tests if the largest contour is correctly detected in a valid hand mask."""
    # Create a synthetic binary mask with a hand-like shape (rectangle)
    hand_mask = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(hand_mask, (50, 50), (150, 150), 255, -1)  # Draw a white square

    contour_mask, largest_contour = main.detect_hand_contours(hand_mask, hand_mask.shape)

    # Assertions
    assert isinstance(contour_mask, np.ndarray), "Contour mask should be a NumPy array."
    assert contour_mask.shape == hand_mask.shape, "Contour mask should have the same shape as the input mask."
    assert len(largest_contour) > 0, "There should be at least one detected contour."
    assert contour_mask.sum() > 0, "The contour mask should not be empty."


def test_detect_hand_contours_with_multiple_shapes():
    """Tests if the function correctly identifies the largest contour among multiple shapes."""
    # Create a binary mask with two shapes: a small and a large rectangle
    hand_mask = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(hand_mask, (50, 50), (100, 100), 255, -1)  # Small rectangle
    cv2.rectangle(hand_mask, (150, 150), (280, 280), 255, -1)  # Large rectangle

    contour_mask, largest_contour = main.detect_hand_contours(hand_mask, hand_mask.shape)

    # Assertions
    assert len(largest_contour) > 0, "There should be a detected contour."
    # The largest contour should correspond to the larger rectangle
    assert cv2.contourArea(largest_contour) > 10000, "The largest contour should correspond to the larger shape."


def test_detect_hand_contours_with_empty_mask():
    """Tests if the function raises a ValueError when no contour is found."""
    # Create an empty binary mask (all zeros)
    empty_mask = np.zeros((200, 200), dtype=np.uint8)

    with pytest.raises(ValueError, match="No hand contour detected."):
        main.detect_hand_contours(empty_mask, empty_mask.shape)


def test_detect_hand_contours_with_noise():
    """Tests if small noise does not affect the detection of the largest contour."""
    # Create a binary mask with a large shape and some noise
    hand_mask = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(hand_mask, (50, 50), (250, 250), 255, -1)  # Large rectangle

    # Add small noise
    for _ in range(10):
        x, y = np.random.randint(0, 300, size=2)
        hand_mask[y, x] = 255  # Random white pixels (noise)

    contour_mask, largest_contour = main.detect_hand_contours(hand_mask, hand_mask.shape)

    # Assertions
    assert len(largest_contour) > 0, "There should be a detected contour."
    assert cv2.contourArea(largest_contour) > 30000, "Noise should not affect the detection of the largest contour."
