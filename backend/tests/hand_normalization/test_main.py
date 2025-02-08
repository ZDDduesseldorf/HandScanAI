import pytest
import numpy as np
import cv2
from pathlib import Path
from unittest.mock import patch
from hand_normalization.src import main

# Run in Terminal with: pytest tests/hand_normalization
# === Global Paths === #
BASE_DIR = Path(__file__).resolve().parent.parent 
TEST_IMAGE_DIR = BASE_DIR / "data" / "TestImages"

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


@pytest.fixture
def dummy_mask():
    """Provides a reusable dummy mask for tests."""
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[1:9, 1:9] = 255
    return mask


@pytest.fixture
def dummy_image():
    """Provides a dummy image for testing."""
    return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)


@pytest.fixture
def dummy_landmarks():
    """Provides dummy hand landmarks for testing."""
    landmarks = [(0, 0)] * 21
    landmarks[3] = (3, 3)    # Thumb
    landmarks[7] = (4, 4)    # Index
    landmarks[11] = (5, 5)   # Middle
    landmarks[13] = (6, 6)   # Hand body
    landmarks[15] = (7, 7)   # Ring
    landmarks[19] = (8, 8)   # Little
    return landmarks


@pytest.fixture
def dummy_region_with_mask(dummy_mask):
    """Provides a dummy region dictionary with a mask for testing."""
    return {"name": "HAND_0", "mask": dummy_mask}


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


@pytest.fixture
def fill_color():
    """Provides a fill color for testing."""
    return (0, 0, 0)  # Schwarzer Hintergrund


# === TESTS FOR get_landmarks === #
def test_get_landmarks_valid_image(valid_image_path):
    """Tests if landmarks are detected in a valid hand image."""
    landmarks = main.get_landmarks(valid_image_path)
    assert isinstance(landmarks, list), "The result should be a list."
    assert all(isinstance(point, tuple) and len(point) == 2 for point in landmarks), (
        "All landmarks should be (x, y) tuples."
    )
    assert len(landmarks) > 0, "There should be at least one detected landmark."


def test_get_landmarks_invalid_path(invalid_image_path):
    """Tests if an invalid path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        main.get_landmarks(invalid_image_path)


def test_get_landmarks_invalid_detection(empty_image):
    """Tests if a ValueError is raised when the number of detected landmarks is incorrect."""
    with pytest.raises(ValueError, match="Expected 21 landmarks"):
        main.get_landmarks(empty_image)


def test_get_landmarks_detects_21_points(valid_image_path):
    """Tests if exactly 21 hand landmarks are detected in a valid hand image."""
    landmarks = main.get_landmarks(valid_image_path)

    assert isinstance(landmarks, list), "The result should be a list."
    assert len(landmarks) == 21, f"Expected 21 landmarks, but got {len(landmarks)}."
    assert all(isinstance(point, tuple) and len(point) == 2 for point in landmarks), \
        "All landmarks should be (x, y) coordinate tuples."


# === TESTS FOR create_handmask === #
def test_create_handmask_with_skin_color_image():
    """Tests if the hand mask correctly identifies skin-colored regions."""
    skin_bgr = np.full((100, 100, 3), (45, 60, 100), dtype=np.uint8)
    mask = main.create_handmask(skin_bgr)

    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == (100, 100), "The mask should have the same spatial dimensions as the input image."
    assert mask.sum() > 0, "The mask should detect skin-colored areas and not be empty."


def test_create_handmask_with_non_skin_color_image():
    """Tests if the hand mask correctly ignores non-skin-colored regions."""
    blue_bgr = np.full((100, 100, 3), (255, 0, 0), dtype=np.uint8)
    mask = main.create_handmask(blue_bgr)

    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == (100, 100), "The mask should have the same spatial dimensions as the input image."
    assert mask.sum() == 0, "The mask should be empty for non-skin-colored regions."


def test_create_handmask_with_empty_image():
    """Tests if the function handles an empty image correctly."""
    empty_image = np.zeros((100, 100, 3), dtype=np.uint8)
    mask = main.create_handmask(empty_image)

    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == (100, 100), "The mask should have the same spatial dimensions as the input image."
    assert mask.sum() == 0, "The mask should be empty for a completely black image."


# === TESTS FOR detect_hand_contours === #
def test_detect_hand_contours_with_valid_mask():
    """Tests if the largest contour is correctly detected in a valid hand mask."""
    hand_mask = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(hand_mask, (50, 50), (150, 150), 255, -1)

    contour_mask, largest_contour = main.detect_hand_contours(hand_mask, hand_mask.shape)

    assert isinstance(contour_mask, np.ndarray), "Contour mask should be a NumPy array."
    assert contour_mask.shape == hand_mask.shape, "Contour mask should have the same shape as the input mask."
    assert len(largest_contour) > 0, "There should be at least one detected contour."
    assert contour_mask.sum() > 0, "The contour mask should not be empty."


def test_detect_hand_contours_with_multiple_shapes():
    """Tests if the function correctly identifies the largest contour among multiple shapes."""
    hand_mask = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(hand_mask, (50, 50), (100, 100), 255, -1) 
    cv2.rectangle(hand_mask, (150, 150), (280, 280), 255, -1)  

    contour_mask, largest_contour = main.detect_hand_contours(hand_mask, hand_mask.shape)

    assert len(largest_contour) > 0, "There should be a detected contour."
    assert cv2.contourArea(largest_contour) > 10000, "The largest contour should correspond to the larger shape."


def test_detect_hand_contours_with_empty_mask():
    """Tests if the function raises a ValueError when no contour is found."""
    empty_mask = np.zeros((200, 200), dtype=np.uint8)

    with pytest.raises(ValueError, match="No hand contour detected."):
        main.detect_hand_contours(empty_mask, empty_mask.shape)


def test_detect_hand_contours_returns_largest_contour():
    """Tests if the function correctly returns the largest contour among multiple shapes."""
    hand_mask = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(hand_mask, (50, 50), (100, 100), 255, -1) 
    cv2.rectangle(hand_mask, (150, 150), (280, 280), 255, -1)

    contour_mask, largest_contour = main.detect_hand_contours(hand_mask, hand_mask.shape)

    # small_area = (100 - 50) * (100 - 50) 
    large_area = (280 - 150) * (280 - 150)

    assert len(largest_contour) > 0, "A contour should be detected."
    assert cv2.contourArea(largest_contour) == large_area, "The detected contour should be the largest one."


# === TESTS FOR detect_largest_defects === #
def test_detect_largest_defects_with_valid_contour():
    """Tests if the function detects convexity defects on a hand-like contour."""
    contour = np.array([
        [[50, 50]],
        [[150, 50]],
        [[150, 150]],
        [[100, 120]], 
        [[50, 150]]
    ], dtype=np.int32)

    defects = main.detect_largest_defects(contour)

    assert isinstance(defects, list), "The result should be a list."
    assert len(defects) > 0, "At least one defect should be detected."
    assert all(isinstance(point, tuple) and len(point) == 2 for point in defects), "Defects should be (x, y) tuples."


def test_detect_largest_defects_with_circle():
    """Tests if a circular contour returns no defects."""
    circle = cv2.ellipse2Poly((100, 100), (50, 50), 0, 0, 360, 10)

    defects = main.detect_largest_defects(circle)

    assert defects == [], "A perfect circle should have no convexity defects."


def test_detect_largest_defects_with_multiple_defects():
    """Tests if the function returns exactly four largest defects when more exist."""
    contour = np.array([
        [[100, 50]],
        [[120, 90]],
        [[160, 100]],
        [[120, 110]],
        [[100, 150]],
        [[80, 110]],
        [[40, 100]],
        [[80, 90]]
    ], dtype=np.int32)

    defects = main.detect_largest_defects(contour)

    assert len(defects) == 4, "The function should return exactly four defects."


# === TESTS FOR contour_to_bitmask === #
def test_contour_to_bitmask_with_rectangle():
    """Tests if a rectangular contour is correctly converted to a binary mask."""
    image_shape = (100, 100)
    rectangle_contour = np.array([[20, 20], [80, 20], [80, 80], [20, 80]])

    mask = main.contour_to_bitmask(rectangle_contour, image_shape)

    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == image_shape, "The mask should match the specified image shape."
    assert mask.sum() > 0, "The mask should contain non-zero values for the filled rectangle."


def test_contour_to_bitmask_with_empty_contour():
    """Tests if the function returns an empty mask for an empty contour."""
    image_shape = (100, 100)
    empty_contour = np.array([])

    mask = main.contour_to_bitmask(empty_contour, image_shape)

    assert isinstance(mask, np.ndarray), "The result should be a NumPy array."
    assert mask.shape == image_shape, "The mask should match the specified image shape."
    assert mask.sum() == 0, "The mask should be completely empty for an empty contour."
    

# === TESTS FOR get_sorted_points_by_distance === #
def test_sorted_points():
    """Tests if points are correctly sorted by distance to the reference point."""
    points = [(5, 5), (1, 1), (3, 3), (0, 0)]
    reference_point = (0, 0)
    
    result = main.get_sorted_points_by_distance(points, reference_point)
    expected = [(0, 0), (1, 1), (3, 3), (5, 5)]

    assert result == expected, f"Expected {expected}, but got {result}."


def test_sorted_points_return_closest():
    """Tests if only the closest point is returned when return_closest=True."""
    points = [(10, 10), (2, 2), (5, 5)]
    reference_point = (0, 0)
    
    result = main.get_sorted_points_by_distance(points, reference_point, return_closest=True)
    expected = (2, 2)

    assert result == expected, f"Expected closest point {expected}, but got {result}."


def test_sorted_points_empty_list():
    """Tests if an empty list returns an empty result."""
    points = []
    reference_point = (0, 0)
    
    result = main.get_sorted_points_by_distance(points, reference_point)
    expected = []

    assert result == expected, "Expected an empty list for empty input."


# === TESTS FOR integrate_defects === #
def test_integrate_defects():
    """Tests if defect points are correctly integrated into the defining points."""
    defining_points = [(np.int32(10), np.int32(10)), (np.int32(20), np.int32(20)), (np.int32(30), np.int32(30))]
    defects = [(np.int32(5), np.int32(5)), (np.int32(15), np.int32(15)), (np.int32(35), np.int32(35))]

    result = main.integrate_defects(defining_points.copy(), defects)
    expected = [(5, 5), (10, 10), (15, 15), (20, 20), (30, 30), (35, 35)]

    assert [(int(x), int(y)) for x, y in result] == expected, f"Expected {expected}, but got {result}."


def test_integrate_defects_with_empty_defining_points():
    """Tests if defects are correctly added when defining points list is empty."""
    defining_points = []
    defects = [(np.int32(1), np.int32(1)), (np.int32(2), np.int32(2)), (np.int32(3), np.int32(3))]

    result = main.integrate_defects(defining_points.copy(), defects)
    expected = [(1, 1), (2, 2), (3, 3)]

    assert [(int(x), int(y)) for x, y in result] == expected, f"Expected {expected}, but got {result}."


def test_integrate_defects_with_insufficient_defects():
    """Tests if the function raises a ValueError when there are fewer than 3 defect points."""
    defining_points = [(np.int32(10), np.int32(10)), (np.int32(20), np.int32(20))]
    defects = [(np.int32(5), np.int32(5))] 

    with pytest.raises(ValueError, match="At least 3 defect points are required."):
        main.integrate_defects(defining_points.copy(), defects)


def test_integrate_defects_with_invalid_point_structure():
    """Tests if the function raises a TypeError when points are not 2D tuples."""
    defining_points = [(np.int32(10), np.int32(10)), (np.int32(20), np.int32(20))]
    defects = [(np.int32(1), np.int32(1)), (np.int32(2), np.int32(2), np.int32(3)), (np.int32(3), np.int32(3))]

    with pytest.raises(TypeError, match="All points must be tuples of two integers \\(x, y\\)."):
        main.integrate_defects(defining_points, defects)


# === TESTS FOR extract_segment_masks === #
def test_extract_segment_masks_single_contour():
    """Tests if a single contour is correctly extracted as a segment mask."""
    mask = np.zeros((10, 10), dtype=np.uint8)
    cv2.rectangle(mask, (2, 2), (7, 7), 255, -1)

    result = main.extract_segment_masks(mask)

    expected_mask = np.zeros((10, 10), dtype=np.uint8)
    cv2.rectangle(expected_mask, (2, 2), (7, 7), 255, -1)

    assert len(result) == 1, f"Expected 1 segment, but got {len(result)}."
    assert np.array_equal(result[0], expected_mask), "The extracted segment mask does not match the expected mask."


def test_extract_segment_masks_multiple_contours():
    """Tests if multiple separate contours are correctly extracted."""
    mask = np.zeros((20, 20), dtype=np.uint8)
    cv2.rectangle(mask, (2, 2), (5, 5), 255, -1)  
    cv2.rectangle(mask, (10, 10), (15, 15), 255, -1) 

    result = main.extract_segment_masks(mask)

    expected_mask1 = np.zeros((20, 20), dtype=np.uint8)
    cv2.rectangle(expected_mask1, (2, 2), (5, 5), 255, -1)

    expected_mask2 = np.zeros((20, 20), dtype=np.uint8)
    cv2.rectangle(expected_mask2, (10, 10), (15, 15), 255, -1)

    assert len(result) == 2, f"Expected 2 segments, but got {len(result)}."
    assert any(np.array_equal(seg, expected_mask1) for seg in result), "First segment mask not correctly extracted."
    assert any(np.array_equal(seg, expected_mask2) for seg in result), "Second segment mask not correctly extracted."


def test_extract_segment_masks_no_contours():
    """Tests if an empty mask returns an empty list."""
    mask = np.zeros((10, 10), dtype=np.uint8)

    result = main.extract_segment_masks(mask)

    assert result == [], "Expected an empty list when no contours are present."


# === TESTS FOR assign_masks_to_regions === #
def test_assign_masks_to_regions(dummy_mask, dummy_landmarks):
    """Tests if masks are correctly assigned to regions based on landmarks."""
    sorted_segments = [dummy_mask for _ in range(7)]  

    result = main.assign_masks_to_regions(sorted_segments, dummy_landmarks)

    assert len(result) == 7, f"Expected 7 regions, but got {len(result)}."
    for region in result:
        assert "mask" in region, f"Region {region['name']} has no mask assigned."
        assert isinstance(region["mask"], np.ndarray), f"Mask in region {region['name']} is not a NumPy array."


def test_assign_masks_to_regions_with_insufficient_segments(dummy_mask):
    """Tests if the function raises a ValueError when there are fewer than 7 masks."""
    sorted_segments = [dummy_mask for _ in range(3)]
    landmarks = [(0, 0)] * 21

    with pytest.raises(ValueError, match="sorted_segments must contain at least 7 masks."):
        main.assign_masks_to_regions(sorted_segments, landmarks)

    
def test_assign_masks_to_regions_with_insufficient_landmarks(dummy_mask):
    """Tests if the function raises a ValueError when there are fewer than 20 landmarks."""
    sorted_segments = [dummy_mask for _ in range(7)]
    landmarks = [(0, 0)] * 10

    with pytest.raises(ValueError, match="landmarks must contain at least 20 points."):
        main.assign_masks_to_regions(sorted_segments, landmarks)


# === TESTS FOR rotate_and_crop_region === #
@patch("hand_normalization.src.main.calculate_hand_orientation", return_value=1)
@patch("hand_normalization.src.main.calculate_region_angle", return_value=45)
@patch("hand_normalization.src.main.rotate_image_no_crop")
@patch("hand_normalization.src.main.get_bounding_box_with_margin", return_value=(25, 25, 75, 75))
@patch("hand_normalization.src.main.crop_to_bounding_box")
def test_rotate_and_crop_region(
    mock_crop, mock_bounding_box, mock_rotate, mock_angle, mock_orientation,
    dummy_region_with_mask, dummy_image, dummy_landmarks
):
    """Tests if the region is correctly rotated and cropped."""

    mock_rotate.side_effect = lambda img, angle: img
    mock_crop.side_effect = lambda img, bbox: img[25:75, 25:75]

    result = main.rotate_and_crop_region(dummy_region_with_mask, dummy_image, dummy_landmarks)

    assert result.shape == (50, 50, 3), f"Expected cropped image of shape (50, 50, 3), but got {result.shape}."
    mock_orientation.assert_called_once_with(dummy_landmarks)
    mock_angle.assert_called_once_with(dummy_region_with_mask["name"], dummy_landmarks, 1)
    assert mock_rotate.call_count == 3, "rotate_image_no_crop should be called three times (for image and mask and the rotationartifacts)."
    mock_bounding_box.assert_called_once()
    mock_crop.assert_called_once()


@patch("hand_normalization.src.main.get_bounding_box_with_margin", return_value=None)
def test_rotate_and_crop_region_no_bounding_box(mock_bounding_box, dummy_region_with_mask, dummy_image, dummy_landmarks):
    """Tests if the function raises a ValueError when no bounding box is found."""

    with pytest.raises(ValueError, match="No valid bounding box found for region: HAND_0"):
        main.rotate_and_crop_region(dummy_region_with_mask, dummy_image, dummy_landmarks)


# === TESTS FOR resize_to_target === #
def test_resize_to_target_with(dummy_image, fill_color):
    """Tests if the dummy image is resized and centered correctly on the canvas."""
    target_size = 224
    result = main.resize_to_target(dummy_image, target_size, fill_color)

    assert result.shape == (target_size, target_size, 3), "The resized image does not match the target size."

    non_fill_area = np.where(np.any(result != fill_color, axis=-1))
    
    assert non_fill_area[0].min() >= (target_size - int(dummy_image.shape[0] * (target_size / max(dummy_image.shape[:2])))), \
        "The image is not correctly aligned at the bottom."


# === TESTS FOR test_normalize_hand_image === #
def test_normalize_hand_image_path(valid_image_path):
    """Tests if the hand normalization has 7 entries."""
    regions_dict = main.normalize_hand_image(valid_image_path)
    
    assert len(regions_dict) == 7


@patch("hand_normalization.src.main.segment_hand_image")
@patch("hand_normalization.src.main.resize_images")
@patch("hand_normalization.src.main.build_regions_dict")
def test_normalize_hand_image(
    mock_build_regions_dict, mock_resize_images, mock_segment_hand_image, valid_image_path
):
    """Tests if normalize_hand_image correctly normalizes the hand image."""
    mock_segment_hand_image.return_value = [{"name": "HAND_0", "image": np.zeros((100, 100, 3), dtype=np.uint8)}]
    mock_resize_images.return_value = [{"name": "HAND_0", "image": np.zeros((224, 224, 3), dtype=np.uint8)}]
    mock_build_regions_dict.return_value = {"HAND_0": np.zeros((224, 224, 3), dtype=np.uint8)}

    result = main.normalize_hand_image(valid_image_path)

    assert isinstance(result, dict), "The result should be a dictionary."
    assert "HAND_0" in result, "The result dictionary should contain the key 'HAND_0'."
    assert result["HAND_0"].shape == (224, 224, 3), "The image should be resized to (224, 224, 3)."

    mock_segment_hand_image.assert_called_once_with(valid_image_path)
    mock_resize_images.assert_called_once_with(mock_segment_hand_image.return_value)
    mock_build_regions_dict.assert_called_once_with(mock_resize_images.return_value)


@patch("hand_normalization.src.main.segment_hand_image")
@patch("hand_normalization.src.main.resize_images")
@patch("hand_normalization.src.main.build_regions_dict")
def test_normalize_hand_image_contains_7_regions(
    mock_build_regions_dict, mock_resize_images, mock_segment_hand_image, valid_image_path
):
    """Tests if normalize_hand_image returns a dictionary with exactly 7 regions."""
    mock_segment_hand_image.return_value = [
        {"name": f"HAND_{i}", "image": np.zeros((100, 100, 3), dtype=np.uint8)} for i in range(7)
    ]

    mock_resize_images.return_value = [
        {"name": f"HAND_{i}", "image": np.zeros((224, 224, 3), dtype=np.uint8)} for i in range(7)
    ]

    mock_build_regions_dict.return_value = {
        f"HAND_{i}": np.zeros((224, 224, 3), dtype=np.uint8) for i in range(7)
    }

    result = main.normalize_hand_image(valid_image_path)

    assert isinstance(result, dict), "The result should be a dictionary."
    assert len(result) == 7, f"The result should contain exactly 7 regions, but got {len(result)}."

    mock_segment_hand_image.assert_called_once_with(valid_image_path)
    mock_resize_images.assert_called_once_with(mock_segment_hand_image.return_value)
    mock_build_regions_dict.assert_called_once_with(mock_resize_images.return_value)
