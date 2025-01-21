import os
from pipelines.regions_utils import HandRegions, PipelineDictKeys
import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Tuple

# TODO: Decide with frontend on final implementation and use of get_landmarks-function.

################################## Debug & Test Utils ##################################


def draw_point(image: np.ndarray, point: Tuple[int, int]) -> None:
    """
    Draws a point on an image and displays the result.

    Args:
        image (np.ndarray): The image on which the point will be drawn.
        point (Tuple[int, int]): The (x, y) coordinates of the point to be drawn.

    Returns:
        None: This function modifies the input image in-place and displays it.
    """
    cv2.circle(image, point, radius=5, color=(0, 255, 0), thickness=-1)
    cv2.imshow("Image with Point", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_images(images: List[np.ndarray]) -> None:
    """
    Displays a list of images sequentially in a window.

    Args:
        images (List[np.ndarray]): A list of images, where each image is represented as a NumPy array.

    Returns:
        None: This function does not return anything. It displays each image in a window until a key is pressed.
    """
    for image in images:
        cv2.imshow("Images", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def draw_images_in_grid(
    image_list: list,
    rows: int,
    cols: int,
    image_size: Tuple[int, int] = (224, 224),
    padding: int = 10,
    bg_color: Tuple[int, int, int] = (13, 17, 23),
) -> np.ndarray:
    """
    Arranges a list of images in a grid format on a single canvas.

    Args:
        image_list (list): List of images as NumPy arrays.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        image_size (Tuple[int, int], optional): Target size (width, height) for resizing each image. Default is (224, 224).
        padding (int, optional): Padding (in pixels) between images in the grid. Default is 10.
        bg_color (Tuple[int, int, int], optional): Background color as a BGR tuple (blue, green, red). Default is (13, 17, 23).

    Returns:
        np.ndarray: The resulting image canvas with the arranged grid of images.

    Notes:
        - If the number of images in `image_list` exceeds `rows * cols`, the excess images will be ignored.
        - Grayscale images in the list are automatically converted to color (BGR format).
        - The canvas size is calculated based on the grid dimensions, image size, and padding.

    Example:
        images = [cv2.imread("image1.jpg"), cv2.imread("image2.jpg")]
        grid = draw_images_in_grid(images, rows=2, cols=2)
        cv2.imshow("Image Grid", grid)
        cv2.waitKey(0)
    """
    canvas_height = rows * (image_size[1] + padding) + padding
    canvas_width = cols * (image_size[0] + padding) + padding

    canvas = np.full((canvas_height, canvas_width, 3), bg_color, dtype=np.uint8)

    for i, img in enumerate(image_list):
        if i >= rows * cols:
            break  # Avoid adding more images than the grid can hold
        if len(img.shape) == 2:  # Check if image is grayscale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img_resized = cv2.resize(img, image_size)

        row = i // cols
        col = i % cols
        y = padding + row * (image_size[1] + padding)
        x = padding + col * (image_size[0] + padding)

        canvas[y : y + image_size[1], x : x + image_size[0]] = img_resized

    return canvas


################################## Image normalization functions ##################################


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

    additional_defects = calculate_additional_defects(region_defining_points, landmarks, contour_mask)
    region_defining_points = integrate_defects(region_defining_points, additional_defects)

    sorted_segments = extract_segements(region_defining_points, original_image, contour_mask, landmarks)
    segmented_regions = assign_regions(sorted_segments, original_image, landmarks)
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

    if len(landmarks) != 21:
        raise ValueError(f"Expected 21 landmarks, but detected {len(landmarks)}.")

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


def calculate_region_defining_points(
    landmarks: List[Tuple[int, int]], contour_mask: np.ndarray, contour: np.ndarray
) -> List[Tuple[int, int]]:
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

    defect_distances = [(defect[0][3], tuple(largest_contour[defect[0][2]][0])) for defect in defects]

    four_largest_defects = [point for _, point in sorted(defect_distances, reverse=True)[:4]]

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

    if contour is not None and len(contour) > 0:
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
    if not points:
        return []

    if isinstance(points[0], int):
        points = [points]

    inside_points = [
        point
        for point in points
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
    index_defect = detect_missing_point(region_defining_points[2], region_defining_points[1], contour_mask, blank)
    pinkie_defect = detect_missing_point(region_defining_points[2], region_defining_points[3], contour_mask, blank)

    return [outer_thumb_defect, index_defect, pinkie_defect]


def detect_missing_point(
    first_defect: Tuple[int, int], second_defect: Tuple[int, int], contour_mask: np.ndarray, blank_image: np.ndarray
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
    detected_point = get_sorted_points_by_distance(intersection_points, moved_point, return_closest=True)

    return detected_point


def find_direction_vector(point1: Tuple[int, int], point2: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculates the direction vector from the first point to the second point in a 2D space.

    Args:
        point1 (Tuple[int, int]): The starting point as (x, y) coordinates.
        point2 (Tuple[int, int]): The ending point as (x, y) coordinates.

    Returns:
        Tuple[int, int]: The direction vector as (dx, dy), where:
                         dx = point2[0] - point1[0]
                         dy = point2[1] - point1[1].
    """
    return (point2[0] - point1[0], point2[1] - point1[1])


def get_sorted_points_by_distance(
    array_of_points: List[Tuple[int, int]], given_point: Tuple[int, int], return_closest: bool = False
) -> List[Tuple[int, int]]:
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


def calculate_euclidean_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """
    Calculates the Euclidean distance between two points in a 2D space.

    Args:
        point1 (Tuple[int, int]): The first point as (x, y) coordinates.
        point2 (Tuple[int, int]): The second point as (x, y) coordinates.

    Returns:
        float: The Euclidean distance between the two points.
    """
    if not (isinstance(point1, (tuple, list)) and isinstance(point2, (tuple, list))):
        raise TypeError("Both points must be tuples or lists of two numerical values.")
    if not (len(point1) == 2 and len(point2) == 2):
        raise ValueError("Both points must contain exactly two elements.")
    
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5


def integrate_defects(region_defining_points, defects):
    """
    Integrates additional defect points into defining points list.

    Args:
        region_defining_points (List[Tuple[int, int]]): Current defining points.
        defects (List[Tuple[int, int]]): Additional defect points.

    Returns:
        List[Tuple[int, int]]: Updated defining points list.

    Raises:
        ValueError: If defects list has fewer than 3 elements.
        TypeError: If inputs are not lists of 2D points (tuples of two integers).
    """
    print(region_defining_points)
    if not isinstance(region_defining_points, list) or not isinstance(defects, list):
        raise TypeError("Both inputs must be lists of (x, y) coordinate tuples.")

    for point in region_defining_points + defects:
        if not (isinstance(point, tuple) and len(point) == 2 and 
                all(isinstance(coord, np.integer) for coord in point)):
            raise TypeError("All points must be tuples of two integers (x, y).")

    if len(defects) < 3:
        raise ValueError("At least 3 defect points are required.")

    region_defining_points.insert(0, defects[0])  
    region_defining_points.insert(2, defects[1])   
    region_defining_points.append(defects[2])      

    return region_defining_points


def extract_segements(region_defining_points, image, contour_mask, landmarks):
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
    segmented_contour_mask = draw_lines_on_mask(contour_mask, region_defining_points)
    hand_segments = extract_segment_masks(segmented_contour_mask)
    sorted_segments = sorted(hand_segments, key=count_white_pixels, reverse=True)[:7]
    return sorted_segments


def draw_lines_on_mask(mask: np.ndarray, points: list, color: int = 255, thickness: int = 2) -> np.ndarray:
    """
    Draws lines connecting points on a given mask.

    Args:
        mask (np.ndarray): The binary mask where lines are drawn.
        points (list): List of (x, y) tuples representing the points to connect.
        color (int): Color of the lines (default is 255 for white).
        thickness (int): Thickness of the lines (default is 2).

    Returns:
        np.ndarray: Updated mask with lines drawn.
    """
    mask_copy = mask.copy()
    for idx in range(len(points) - 1):
        cv2.line(mask_copy, points[idx], points[idx + 1], color, thickness)
    return mask_copy


def extract_segment_masks(mask: np.ndarray) -> list:
    """
    Extracts individual segment masks from a binary mask.

    Args:
        mask (np.ndarray): Binary mask from which contours are extracted.

    Returns:
        list: List of binary masks, each representing a separate segment.
    """
    hand_segments = []
    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        segment_mask = contour_to_bitmask(contour, mask.shape)
        hand_segments.append(segment_mask)
    return hand_segments


def count_white_pixels(image: np.ndarray) -> int:
    """
    Counts the number of white pixels (value 255) in a binary or grayscale image.

    Args:
        image (np.ndarray): The input image as a NumPy array. Expected to be a binary
                            or grayscale image where white pixels have the value 255.

    Returns:
        int: The total count of white pixels in the image.
    """
    return np.sum(image == 255)


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
    regions = assign_masks_to_regions(sorted_segments, landmarks)

    for region in regions:
        cropped_image = rotate_and_crop_region(region, image, landmarks)
        region.update({"segment_image": cropped_image})

    return [{"name": region["name"], "image": region["segment_image"]} for region in regions]


def assign_masks_to_regions(sorted_segments, landmarks) -> list:
    """
    Assigns masks to specific regions based on reference points.

    Args:
        sorted_segments (list): List of sorted masks.
        landmarks (list): List of landmarks.

    Returns:
        list: List of regions with assigned masks.

    Raises:
        ValueError: If sorted_segments has fewer than 7 masks.
        ValueError: If landmarks has fewer than 20 points.
        TypeError: If inputs are not lists or masks are not numpy arrays.
    """
    if not isinstance(sorted_segments, list) or not all(isinstance(mask, np.ndarray) for mask in sorted_segments):
        raise TypeError("sorted_segments must be a list of NumPy arrays.")
    
    if not isinstance(landmarks, list) or not all(isinstance(point, tuple) and len(point) == 2 for point in landmarks):
        raise TypeError("landmarks must be a list of (x, y) coordinate tuples.")

    if len(sorted_segments) < 7:
        raise ValueError("sorted_segments must contain at least 7 masks.")

    if len(landmarks) < 20:
        raise ValueError("landmarks must contain at least 20 points.")
    
    regions = [
        {"name": HandRegions.HAND_0.value, "reference_point": []},
        {"name": HandRegions.HANDBODY_1.value, "reference_point": landmarks[13]},
        {"name": HandRegions.THUMB_2.value, "reference_point": landmarks[3]},
        {"name": HandRegions.INDEXFINGER_3.value, "reference_point": landmarks[7]},
        {"name": HandRegions.MIDDLEFINGER_4.value, "reference_point": landmarks[11]},
        {"name": HandRegions.RINGFINGER_5.value, "reference_point": landmarks[15]},
        {"name": HandRegions.LITTLEFINGER_6.value, "reference_point": landmarks[19]},
    ]

    regions[0].update({"mask": sorted_segments[0]})
    for region in regions[1:]:
        region_reference_point = region["reference_point"]
        for segments in sorted_segments[1:]:
            points_in_segment = points_in_mask(segments, region_reference_point)
            if points_in_segment:
                region.update({"mask": segments})
    return regions


def rotate_and_crop_region(region, image, landmarks) -> np.ndarray:
    """
    Rotates and crops a single region based on its mask and orientation.

    Args:
        region (dict): Region containing mask and name.
        image (np.ndarray): Original image.
        landmarks (list): Hand landmarks.

    Returns:
        np.ndarray: Cropped and rotated image segment.
    """
    orientation_hand = calculate_hand_orientation(landmarks)
    angle = calculate_region_angle(region["name"], landmarks, orientation_hand)

    rotated_image = rotate_image_no_crop(image, angle)
    rotated_mask = rotate_image_no_crop(region["mask"], angle)

    bounding_box = get_bounding_box_with_margin(rotated_mask, 5)
    if bounding_box is None:
        raise ValueError(f"No valid bounding box found for region: {region['name']}")

    cropped_image = crop_to_bounding_box(rotated_image, bounding_box)
    return cropped_image


def calculate_hand_orientation(landmarks: list) -> int:
    """
    Determines the hand orientation based on ring and index finger base landmarks.

    Args:
        landmarks (list): List of hand landmarks, where each landmark is a tuple (x, y).

    Returns:
        int: Orientation of the hand. Returns -1 if the ring finger base is to the right
             of the index finger base (thumb on the left side), otherwise 1.
    """
    ring_finger_base = landmarks[13]
    index_finger_base = landmarks[5]
    return -1 if ring_finger_base[0] > index_finger_base[0] else 1


def calculate_region_angle(region_name: str, landmarks: list, orientation_hand: int) -> float:
    """
    Calculates the rotation angle for a specific hand region based on its name and landmarks.

    Args:
        region_name (str): The name of the hand region (e.g., HAND_0, THUMB_2).
        landmarks (list): List of hand landmarks, where each landmark is a tuple (x, y).
        orientation_hand (int): Orientation of the hand, typically -1 or 1, based on thumb position.

    Returns:
        float: The calculated rotation angle in degrees for the specified region. Returns
               a default angle of 90 degrees if the region name is not recognized.
    """
    if region_name == HandRegions.HAND_0.value or region_name == HandRegions.HANDBODY_1.value:
        return 90 - calculate_vector_angle(landmarks[5], landmarks[13])
    elif region_name == HandRegions.THUMB_2.value:
        return 180 - calculate_vector_angle(landmarks[2], landmarks[4])
    elif region_name == HandRegions.INDEXFINGER_3.value:
        return 180 - calculate_vector_angle(landmarks[6], landmarks[8])
    elif region_name == HandRegions.MIDDLEFINGER_4.value:
        return 180 - calculate_vector_angle(landmarks[10], landmarks[12])
    elif region_name == HandRegions.RINGFINGER_5.value:
        return 180 - calculate_vector_angle(landmarks[14], landmarks[16])
    elif region_name == HandRegions.LITTLEFINGER_6.value:
        return 180 - calculate_vector_angle(landmarks[18], landmarks[20])
    return 90


def calculate_vector_angle(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """
    Calculates the angle of a vector defined by two points in a 2D space.

    Args:
        point1 (Tuple[int, int]): The starting point of the vector as (x, y) coordinates.
        point2 (Tuple[int, int]): The ending point of the vector as (x, y) coordinates.

    Returns:
        float: The angle of the vector in degrees, measured counterclockwise from the positive x-axis.
    """
    vector = (point2[0] - point1[0], point2[1] - point1[1])
    vector_angle = cv2.fastAtan2(vector[0], vector[1])
    return vector_angle


def rotate_image_no_crop(image: np.ndarray, angle: float, center_of_rotation: list = []) -> np.ndarray:
    """
    Rotates an image around a specified center without cropping the edges.

    Args:
        image (np.ndarray): The input image to be rotated.
        angle (float): The rotation angle in degrees (clockwise is positive).
        center_of_rotation (list, optional): The center point for the rotation as [x, y].
                                             If not provided, the image center is used.

    Returns:
        np.ndarray: The rotated image with adjusted dimensions to prevent cropping.
    """
    angle = float(angle)
    (h, w) = image.shape[:2]
    if center_of_rotation == []:
        center_of_rotation = (w // 2, h // 2)

    rotation_matrix = cv2.getRotationMatrix2D(center_of_rotation, angle, scale=1.0)

    cos = abs(rotation_matrix[0, 0])
    sin = abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    rotation_matrix[0, 2] += (new_w / 2) - center_of_rotation[0]
    rotation_matrix[1, 2] += (new_h / 2) - center_of_rotation[1]

    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))

    return rotated_image


def get_bounding_box_with_margin(mask, margin=0):
    """
    Calculate a bounding box around a mask with an added margin.

    Parameters:
    mask (numpy.ndarray): Binary mask with non-zero values for the region of interest.
    margin (int): Margin to add around the bounding box.

    Returns:
    (x, y, w, h): Tuple representing the bounding box coordinates with the margin.
                    (x, y) is the top-left corner, and (w, h) are the width and height.
    """
    mask = (mask > 0).astype(np.uint8)

    x, y, w, h = cv2.boundingRect(mask)

    x = max(x - margin, 0)
    y = max(y - margin, 0)
    w = min(w + 2 * margin, mask.shape[1] - x)
    h = min(h + 2 * margin, mask.shape[0] - y)

    return x, y, w, h


def crop_to_bounding_box(image, bounding_box):
    """
    Crop an image to a bounding box.

    Parameters:
    image (numpy.ndarray): The input image.
    x, y (int): Top-left corner coordinates of the bounding box.
    w, h (int): Width and height of the bounding box.

    Returns:
    numpy.ndarray: The cropped image.
    """
    x, y, w, h = bounding_box
    cropped_image = image[y : y + h, x : x + w]
    return cropped_image


def resize_images(
    images_with_names: List[Dict[str, np.ndarray]], size: int = 224, fill_color: Tuple[int, int, int] = (255, 255, 255)
) -> List[Dict[str, np.ndarray]]:
    """
    Resizes a list of images to a square target size with optional padding.

    Args:
        images_with_names (List[Dict[str, np.ndarray]]): A list of dictionaries, where each dictionary contains:
            "name" (str): The name of the image or region.
            "image" (np.ndarray): The image data as a NumPy array.
        size (int, optional): The target size of the output image (height and width will be equal). Defaults to 224.
        fill_color (Tuple[int, int, int], optional): The RGB color used to fill padding areas. Defaults to white (255, 255, 255).

    Returns:
        List[Dict[str, np.ndarray]]: A list of dictionaries, where each dictionary contains:
            "name" (str): The name of the image or region.
            "image" (np.ndarray): The resized and padded image as a NumPy array.
    """
    return [
        {"name": region["name"], "image": resize_to_target(region["image"], size, fill_color)}
        for region in images_with_names
    ]


def resize_to_target(input_image: np.ndarray, size: int, fill_color: Tuple[int, int, int]) -> np.ndarray:
    """
    Resizes the input image to fit within a square canvas of the target resolution, maintaining its aspect ratio.
    The resized image is placed on the canvas, aligned to the bottom center. Empty areas are filled with the specified color.

    Args:
        input_image (np.ndarray): The input image to be resized, as a NumPy array.
        size (int): The target resolution for the square canvas (e.g., 224 for a 224x224 canvas).
        fill_color (Tuple[int, int, int]): The color to fill the empty areas, specified as a (B, G, R) tuple.

    Returns:
        np.ndarray: The resized image placed on a square canvas with the specified background color.
    """
    original_height, original_width = input_image.shape[:2]
    if original_width > original_height:
        new_width = size
        new_height = int(original_height * (size / original_width))
    else:
        new_height = size
        new_width = int(original_width * (size / original_height))

    resized_image = cv2.resize(input_image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    new_image = np.full((size, size, 3), fill_color, dtype=np.uint8)

    top_left_x = (size - new_width) // 2
    top_left_y = size - new_height

    new_image[top_left_y : top_left_y + new_height, top_left_x : top_left_x + new_width] = resized_image

    new_image = replace_color_in_range(new_image, [0, 0, 0], [15, 15, 15], [255, 255, 255])

    return new_image


def replace_color_in_range(input_image: np.ndarray, lower_bound: Tuple[int, int, int], upper_bound: Tuple[int, int, int], replacement_color: Tuple[int, int, int]) -> np.ndarray:
    """
    Replaces all pixels in the specified color range with a replacement color.

    Args:
        input_image (np.ndarray): The input image as a NumPy array.
        lower_bound (Tuple[int, int, int]): Lower bound of the color range (B, G, R).
        upper_bound (Tuple[int, int, int]): Upper bound of the color range (B, G, R).
        replacement_color (Tuple[int, int, int]): The color to replace pixels in the range with (B, G, R).

    Returns:
        np.ndarray: The image with pixels in the specified range replaced.
    """
    lower_bound_np = np.array(lower_bound, dtype=np.uint8)
    upper_bound_np = np.array(upper_bound, dtype=np.uint8)

    mask = cv2.inRange(input_image, lower_bound_np, upper_bound_np)

    input_image[mask > 0] = replacement_color

    return input_image


def build_regions_dict(regions: List[Dict[str, np.ndarray]]) -> Dict[str, np.ndarray]:
    """
    Builds a dictionary from region segments.

    Args:
        regions: List of regions with images.

    Returns:
        Dict[str, np.ndarray]: Dictionary of region names and corresponding images.
    """
    return {region["name"]: region["image"] for region in regions}

