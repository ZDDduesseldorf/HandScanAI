import os
import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Tuple
import functions
from enum import Enum

# TODO: Fix region_defining_points @ segment_hand_image func


class HandRegions(Enum):
    """
    Used as region keys to
    - save and load data
    - in dicts that pass data down the pipelines.
    """

    HAND_0 = "Hand"
    HANDBODY_1 = "HandBody"
    THUMB_2 = "Thumb"
    INDEXFINGER_3 = "IndexFinger"
    MIDDLEFINGER_4 = "MiddleFinger"
    RINGFINGER_5 = "RingFinger"
    LITTLEFINGER_6 = "LittleFinger"


def normalize_hand_image(image_path: str) -> Dict[str, np.ndarray]:
    """
    Normalizes a hand image by segmenting, resizing, and returning the image regions as a dictionary.

    Args:
        image_path (str): Path to the input image.

    Returns:
        Dict[str, np.ndarray]: Dictionary containing region names as keys and resized image arrays as values.
    """
    segmented_image_list = segment_hand_image(image_path)
    resized_image_list = resize_images(segmented_image_list)
    normalized_hand_dict = build_regions_dict(resized_image_list)
    return normalized_hand_dict


def segment_hand_image(image_path: str) -> List[Dict[str, np.ndarray]]:
    """
    Segments the input image into hand regions and prepares them for normalization.

    Args:
        image_path (str): Path to the input image.

    Returns:
        List[Dict[str, np.ndarray]]: List of dictionaries with region names and segmented images.
    """
    original_image = load_image(image_path)
    landmarks = get_landmarks(image_path)
    hand_mask = create_handmask(original_image)

    contour_mask, largest_contour = detect_hand_contours(hand_mask, original_image.shape)
    region_defining_points = calculate_region_defining_points(landmarks, contour_mask, largest_contour)

    # Detect missing defects
    additional_defects = calculate_additional_defects(region_defining_points, landmarks, contour_mask)
    region_defining_points = integrate_defects(region_defining_points, additional_defects)

    segmented_regions = extract_hand_segments(region_defining_points, original_image, contour_mask, landmarks)
    return segmented_regions


def load_image(image_path: str) -> np.ndarray:
    """
    Loads an image from a file path and checks validity.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: Loaded image.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    return image


def get_landmarks(image_path: str) -> List[Tuple[int, int]]:
    """
    Detects hand landmarks using MediaPipe Hands.

    Args:
        image_path (str): Path to the image file.

    Returns:
        List[Tuple[int, int]]: List of (x, y) coordinates for landmarks.
    """
    mp_hands = mp.solutions.hands
    image = load_image(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    landmarks = []
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        results = hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    h, w, _ = image.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    landmarks.append((x, y))

    return landmarks


def create_handmask(image: np.ndarray) -> np.ndarray:
    """
    Creates a binary hand mask based on HSV color range.

    Args:
        image (np.ndarray): Original input image.

    Returns:
        np.ndarray: Binary mask of hand region.
    """
    blurred = cv2.GaussianBlur(image, (11, 11), 2)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 40, 80])
    upper_skin = np.array([20, 255, 255])
    return cv2.inRange(hsv, lower_skin, upper_skin)


def detect_hand_contours(hand_mask: np.ndarray, image_shape: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Finds the largest contour in the hand mask.

    Args:
        hand_mask (np.ndarray): Binary mask of the hand.
        image_shape (Tuple[int, int]): Shape of the original image.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Contour mask and largest contour.
    """
    blank = np.zeros(image_shape[:2], dtype=np.uint8)
    contours, _ = cv2.findContours(hand_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No hand contour detected.")
    largest_contour = max(contours, key=cv2.contourArea)
    cv2.drawContours(blank, [largest_contour], -1, 255, 2)
    return blank, largest_contour


def calculate_region_defining_points(landmarks: List[Tuple[int, int]], contour_mask: np.ndarray, contour: np.ndarray) -> List[Tuple[int, int]]:
    """
    Calculates region-defining points from landmarks.

    Args:
        landmarks (List[Tuple[int, int]]): List of hand landmarks.
        contour_mask (np.ndarray): Binary mask of hand contour.

    Returns:
        List[Tuple[int, int]]: Region-defining points.
    """
    lookup_areas = [
        [landmarks[5], landmarks[1], landmarks[2], landmarks[3]],
        [landmarks[5], landmarks[6], landmarks[10], landmarks[9]],
        [landmarks[9], landmarks[10], landmarks[14], landmarks[13]],
        [landmarks[13], landmarks[14], landmarks[18], landmarks[17]],
    ]

    largest_defects = detect_largest_defects(contour)
    defining_points = []

    for area in lookup_areas:
        mask = contour_to_bitmask(np.array(area), contour_mask.shape)
        points = points_in_mask(mask, largest_defects)
        defining_points.append(points[0])
        print(defining_points)
    return defining_points


def detect_largest_defects(largest_contour):
    """
    Detect the four largest convexity defects in the largest contour.

    Args:
        largest_contour: A NumPy array representing the contour.

    Returns:
        List[Tuple[int, int]]: Coordinates of the four largest defect points.
    """
    hull = cv2.convexHull(largest_contour, returnPoints=False)
    defects = cv2.convexityDefects(largest_contour, hull)

    if defects is None or len(defects) == 0:
        return []

    defect_distances = [
        (defect[0][3], tuple(largest_contour[defect[0][2]][0]))
        for defect in defects
    ]

    four_largest_defects = [
        point for _, point in sorted(defect_distances, reverse=True)[:4]
    ]

    return four_largest_defects


def contour_to_bitmask(contour, image_shape):
    """
    Converts a contour or convex hull into a bitmask.

    Args:
        contour (numpy.ndarray): Array of points representing the contour/hull.
        image_shape (tuple): Shape of the output mask (height, width).

    Returns:
        numpy.ndarray: A binary mask with the contour filled.
    """
    mask = np.zeros(image_shape, dtype=np.uint8)
    cv2.fillPoly(mask, [contour], color=255) 

    return mask


def points_in_mask(mask: np.ndarray, points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Checks if points are inside a given binary mask.

    Args:
        mask (np.ndarray): Binary mask (2D NumPy array).
        points (List[Tuple[int, int]]): List of (x, y) coordinates or a single point.

    Returns:
        List[Tuple[int, int]]: List of points that are inside the mask.
    """
    if isinstance(points[0], int):
        points = [points]

    inside_points = [
        point for point in points
        if 0 <= point[0] < mask.shape[1] and 0 <= point[1] < mask.shape[0] and mask[point[1], point[0]] > 0
    ]

    return inside_points


def calculate_additional_defects(region_defining_points, landmarks, contour_mask):
    """
    Detects missing defect points using the hand contour.

    Args:
        region_defining_points: Current defining points.
        landmarks: Hand landmarks.
        contour_mask: Binary mask of hand contour.

    Returns:
        List[Tuple[int, int]]: Additional defect points.
    """
    blank = np.zeros_like(contour_mask)
    outer_thumb_defect = detect_missing_point(region_defining_points[0], landmarks[2], contour_mask, blank)
    print(outer_thumb_defect)

    index_defect = detect_missing_point(region_defining_points[2], region_defining_points[1], contour_mask, blank)
    pinkie_defect = detect_missing_point(region_defining_points[2], region_defining_points[3], contour_mask, blank)
    return [outer_thumb_defect, index_defect, pinkie_defect]


def detect_missing_point(
    first_defect: Tuple[int, int],
    second_defect: Tuple[int, int],
    contour_mask: np.ndarray,
    blank_image: np.ndarray
) -> Tuple[int, int]:
    """
    Detects a missing point between two defects using a direction vector 
    and finds the closest intersection point on the contour.

    Args:
        first_defect (Tuple[int, int]): Coordinates of the first defect point (x, y).
        second_defect (Tuple[int, int]): Coordinates of the second defect point (x, y).
        contour_mask (np.ndarray): Binary mask representing the contour.
        blank_image (np.ndarray): Empty image used for drawing operations.

    Returns:
        Tuple[int, int]: The coordinates of the detected missing point.
    """
    direction_vector = find_direction_vector(first_defect, second_defect)
    moved_point = (
        int(first_defect[0] + direction_vector[0] * 3),
        int(second_defect[1] + direction_vector[1] * 3),
    )

    line_mask = cv2.line(blank_image.copy(), first_defect, moved_point, 255, 1)

    intersection_mask = cv2.bitwise_and(contour_mask, line_mask)
    intersection_coords = np.column_stack(np.where(intersection_mask == 255))

    intersection_points: List[Tuple[int, int]] = [(x, y) for y, x in intersection_coords]
    detected_point = get_sorted_points_by_distance(intersection_points, moved_point)

    return detected_point


def find_direction_vector(point1, point2):
    return (point2[0] - point1[0], point2[1] - point1[1])


def get_sorted_points_by_distance(array_of_points: List[Tuple[int, int]], given_point: Tuple[int, int], return_closest: bool = False) -> List[Tuple[int, int]]:
    """
    Sorts a list of 2D points by their distance to a given reference point.
    Optionally returns only the closest point.

    Args:
        array_of_points (List[Tuple[int, int]]): List of points (x, y).
        given_point (Tuple[int, int]): Reference point (x, y).
        return_closest (bool): If True, returns only the closest point.

    Returns:
        List[Tuple[int, int]] or Tuple[int, int]: Sorted list of points or the closest point.
    """
    sorted_points = sorted(array_of_points, key=lambda point: calculate_euclidean_distance(point, given_point))

    if return_closest:
        return sorted_points[0]
    return sorted_points


def calculate_euclidean_distance(point1, point2):
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** (0.5)


def integrate_defects(region_defining_points, defects):
    """
    Integrates additional defect points into defining points list.

    Args:
        region_defining_points (List[Tuple[int, int]]): Current defining points.
        defects (List[Tuple[int, int]]): Additional defect points.

    Returns:
        List[Tuple[int, int]]: Updated defining points list.
    """
    region_defining_points.insert(0, defects[0])
    region_defining_points.insert(2, defects[1])
    region_defining_points.append(defects[2])
    return region_defining_points


def extract_hand_segments(region_defining_points, image, contour_mask, landmarks):
    """
    Extracts individual hand segments and assigns to regions.

    Args:
        region_defining_points: Defining points for hand segmentation.
        largest_contour: The largest contour of the hand.
        image: Original image.
        landmarks: Hand landmarks.

    Returns:
        List[Dict[str, np.ndarray]]: List of segmented hand regions.
    """
    segmented_contour_mask = contour_mask.copy()
    print(np.sum(segmented_contour_mask))
    for idx in range(len(region_defining_points) - 1):
        cv2.line(segmented_contour_mask, region_defining_points[idx], region_defining_points[idx + 1], 255, 2)

    hand_segments = []
    contours, _ = cv2.findContours(segmented_contour_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        mask = contour_to_bitmask(contour, segmented_contour_mask.shape)
        hand_segments.append(mask)

    sorted_segments = sorted(hand_segments, key=functions.count_white_pixels, reverse=True)[:7]
    return assign_regions(sorted_segments, image, landmarks)


def calculate_hand_orientation(landmarks):
    """
    Determine hand orientation based on ring and index finger base landmarks.
    """
    ring_finger_base = landmarks[13]
    index_finger_base = landmarks[5]
    return -1 if ring_finger_base[0] > index_finger_base[0] else 1


def calculate_region_angle(region_name, landmarks, orientation_hand):
    """
    Calculate the rotation angle for a specific hand region.
    """
    if region_name == (HandRegions.HAND_0.value or HandRegions.HANDBODY_1.value):
        return 90 - orientation_hand * functions.vector_angle(landmarks[5], landmarks[13])
    elif region_name == HandRegions.THUMB_2.value:
        return 180 - functions.vector_angle(landmarks[2], landmarks[4])
    elif region_name == HandRegions.INDEXFINGER_3.value:
        return 180 - functions.vector_angle(landmarks[6], landmarks[8])
    elif region_name == HandRegions.MIDDLEFINGER_4.value:
        return 180 - functions.vector_angle(landmarks[10], landmarks[12])
    elif region_name == HandRegions.RINGFINGER_5.value:
        return 180 - functions.vector_angle(landmarks[14], landmarks[16])
    elif region_name == HandRegions.LITTLEFINGER_6.value:
        return 180 - functions.vector_angle(landmarks[18], landmarks[20])
    return 90  # Default angle for unknown regions


def assign_regions(sorted_segments, image, landmarks):
    """
    Assigns masks to specific hand regions and computes rotated/cropped images.

    Args:
        sorted_segments: Segmented masks.
        image: Original image.
        landmarks: Hand landmarks.

    Returns:
        List[Dict[str, np.ndarray]]: Regions with segment images.
    """
    orientation_hand = calculate_hand_orientation(landmarks)

    regions = [
        {"name": HandRegions.HAND_0.value, "reference_point": []},
        {"name": HandRegions.HANDBODY_1.value, "reference_point": landmarks[13]},
        {"name": HandRegions.THUMB_2.value, "reference_point": landmarks[3]},
        {"name": HandRegions.INDEXFINGER_3.value, "reference_point": landmarks[7]},
        {"name": HandRegions.MIDDLEFINGER_4.value, "reference_point": landmarks[11]},
        {"name": HandRegions.RINGFINGER_5.value, "reference_point": landmarks[15]},
        {"name": HandRegions.LITTLEFINGER_6.value, "reference_point": landmarks[19]},
    ]

    # Assign the masks to regions by checking reference points
    for region in regions:
        for segment in sorted_segments:
            if region["reference_point"]:
                if points_in_mask(segment, region["reference_point"]):
                    region.update({"mask": segment})
                    break
            else:
                region.update({"mask": sorted_segments[0]})  # Whole hand image
    
    # Rotate and crop the images for each region
    for region in regions:
        angle = calculate_region_angle(region["name"], landmarks, orientation_hand)
        mask = region["mask"]
        
        rotated_image = functions.rotate_image_no_crop(image, angle)
        rotated_mask = functions.rotate_image_no_crop(mask, angle)
        bounding_box = functions.get_bounding_box_with_margin(rotated_mask, 5)
        cropped_image = functions.crop_to_bounding_box(rotated_image, bounding_box)
        
        region.update({"segment_image": cropped_image})

    
    # Return the final result
    return [{"name": region["name"], "image": region["segment_image"]} for region in regions]


def resize_images(images_with_names: List[Dict[str, np.ndarray]], size: int = 224, fill_color: Tuple[int, int, int] = (255, 255, 255)) -> List[Dict[str, np.ndarray]]:
    """
    Resizes images to a square target size with padding.

    Args:
        images_with_names: List of region dictionaries with images.
        size: Target image size.
        fill_color: Padding fill color.

    Returns:
        List[Dict[str, np.ndarray]]: Resized images.
    """
    return [{
        "name": region["name"],
        "image": functions.dynamic_resize_image_to_target(region["image"], size, fill_color)
    } for region in images_with_names]


def build_regions_dict(regions: List[Dict[str, np.ndarray]]) -> Dict[str, np.ndarray]:
    """
    Builds a dictionary from region segments.

    Args:
        regions: List of regions with images.

    Returns:
        Dict[str, np.ndarray]: Dictionary of region names and corresponding images.
    """
    return {region["name"]: region["image"] for region in regions}


image_path = "C:\\Users\lukas\Documents\Hand_0000064.jpg"
images = normalize_hand_image(image_path)
image_list = []
for _, image in images.items():
    image_list.append(image)

grid_image = functions.draw_images_in_grid(image_list, rows=1, cols=7, image_size=(244, 244), bg_color=(23, 17, 13))

cv2.imshow('Image Grid', grid_image)
cv2.waitKey(0)
cv2.destroyAllWindows()