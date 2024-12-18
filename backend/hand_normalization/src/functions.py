import cv2
import mediapipe as mp
import numpy as np


def getLandmarks(image_path):
    """
    Use mediapipe to lokate the image coordinates of a hand landmarks image.

    Args:
        image_path (string): path to image

    Returns:
        numpy.ndarray: Landmark Name, x-coordinate, y-coordinate
    """
    # Initialize MediaPipe Hands and Drawing utilities
    mp_hands = mp.solutions.hands
    # Load image
    image = cv2.imread(image_path)
    # Convert the image to RGB as MediaPipe expects RGB input
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    output = []

    # Set up the Hands model in static image mode
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        # Process the image to find hand landmarks
        results = hands.process(image_rgb)

        # Check if any hand landmarks were detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Loop through each landmark, get its name and coordinates
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    # Get the coordinates in image dimensions
                    h, w, _ = image.shape  # Get image dimensions
                    x, y = int(landmark.x * w), int(landmark.y * h)  # Scale x, y to image dimensions

                    output.append([x, y])
    return output


# Function to calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** (0.5)


def find_direction_vector(point1, point2):
    return (point2[0] - point1[0], point2[1] - point1[1])


# Function to sort points by their distance to a given point
def sort_points_by_closeness(array_of_points, given_point):
    """
    Sort a list of 2D points by their distance to a given reference point.

    Args:
        array_of_points (list of tuples): List of tuples where each tuple (x, y) represents a point in 2D space.
        given_point (tuple): A tuple (x, y) representing the reference point.

    Returns:
        list of tuples: List of points sorted by their Euclidean distance to the given point.
    """
    # Sort the array of points by the distance to the given point
    sorted_points = sorted(array_of_points, key=lambda point: euclidean_distance(point, given_point))
    return sorted_points


# Function to find the closest point in an array to a given point
def find_closest_point(array_of_points, given_point):
    return sort_points_by_closeness(array_of_points, given_point)[0]


def hull_or_contour_to_bitmask(contour, image_shape):
    """
    Converts a contour or convex hull into a bitmask.

    Args:
        contour (numpy.ndarray): Array of points representing the contour/hull.
        image_shape (tuple): Shape of the output mask (height, width).

    Returns:
        numpy.ndarray: A binary mask with the contour filled.
    """
    # Create a blank mask with the same shape as the specified image shape
    mask = np.zeros(image_shape, dtype=np.uint8)

    # Fill the contour on the mask
    cv2.fillPoly(mask, [contour], color=255)  # Fill with white color (255)

    return mask


def calculate_center_of_mass(binary_image):
    """
    Calculates the center of mass(CoM) via the highest pixel density of a binary image.

    Args:
        binary_image (tbd?): binary image
    Returns:
        2D_point (tuple): Center of mass in image coordinates.
    """

    # Berechne die Momente des binären Bildes
    moments = cv2.moments(binary_image)

    # Überprüfe, ob M00 nicht null ist, um eine Division durch Null zu vermeiden
    if moments["m00"] != 0:
        # Berechne x und y des Schwerpunktes
        x_com = int(moments["m10"] / moments["m00"])
        y_com = int(moments["m01"] / moments["m00"])
        return (x_com, y_com)
    else:
        # Falls kein CoM berechnet werden kann, gib None zurück
        return None


def rotate_image(image, angle):
    # Get the dimensions of the image
    (h, w) = image.shape[:2]

    # Define the center of the image as the point of rotation
    center = (w // 2, h // 2)

    # Create the rotation matrix using the specified angle
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)

    # Perform the actual rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))

    return rotated_image


def rotate_image_no_crop(image, angle, center_of_rotation=[]):
    angle = float(angle)
    (h, w) = image.shape[:2]
    if center_of_rotation == []:
        center_of_rotation = (w // 2, h // 2)

    # Calculate the rotation matri
    rotation_matrix = cv2.getRotationMatrix2D(center_of_rotation, angle, scale=1.0)

    # Calculate the new bounding dimensions of the image
    cos = abs(rotation_matrix[0, 0])
    sin = abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to account for translation
    rotation_matrix[0, 2] += (new_w / 2) - center_of_rotation[0]
    rotation_matrix[1, 2] += (new_h / 2) - center_of_rotation[1]

    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))

    return rotated_image


def check_points_in_mask(mask, points):
    # Create a blank canvas (black image) of the same size as the mask
    canvas = np.zeros_like(mask, dtype=np.uint8)

    # List to store the points that are inside the mask
    inside_points = []

    # If the list only contains 1 point
    if len(points) == 2 and isinstance(points[0], int):
        point = points
        # Draw the point on the canvas (white pixel)
        cv2.circle(canvas, point, 1, (255), -1)  # Draw a small white dot at the point

        # Check if the mask has a non-zero value at this point
        if mask[point[1], point[0]] > 0:  # Use (x, y) for the index
            inside_points.append(point)
    else:
        for point in points:
            # Draw the point on the canvas (white pixel)
            cv2.circle(canvas, point, 1, (255), -1)  # Draw a small white dot at the point

            # Check if the mask has a non-zero value at this point
            if mask[point[1], point[0]] > 0:  # Use (x, y) for the index
                inside_points.append(point)

    return inside_points


def get_bounding_box_with_margin(mask, margin=0):
    """
    Calculate a bounding box around a mask with an added margin.

    Parameters:
    - mask (numpy.ndarray): Binary mask with non-zero values for the region of interest.
    - margin (int): Margin to add around the bounding box.

    Returns:
    - (x, y, w, h): Tuple representing the bounding box coordinates with the margin.
                    (x, y) is the top-left corner, and (w, h) are the width and height.
    """
    # Ensure the mask is binary
    mask = (mask > 0).astype(np.uint8)  # Convert to binary if needed

    # Step 1: Find the bounding box of the mask
    x, y, w, h = cv2.boundingRect(mask)

    # Step 2: Add the margin to the bounding box
    x = max(x - margin, 0)
    y = max(y - margin, 0)
    w = min(w + 2 * margin, mask.shape[1] - x)
    h = min(h + 2 * margin, mask.shape[0] - y)

    return x, y, w, h


def crop_to_bounding_box(image, bounding_box):
    """
    Crop an image to a bounding box.

    Parameters:
    - image (numpy.ndarray): The input image.
    - x, y (int): Top-left corner coordinates of the bounding box.
    - w, h (int): Width and height of the bounding box.

    Returns:
    - numpy.ndarray: The cropped image.
    """
    x, y, w, h = bounding_box
    # Crop the image using array slicing
    cropped_image = image[y : y + h, x : x + w]
    return cropped_image


def slice_contour(contour_point_list, point1, point2):
    """
    Slices the contour based on two points.
    The result will be a contour from point2 to point1 (or the other way around, depending on order).
    """

    # Find indices of point1 and point2 in the contour
    idx1 = np.where(np.all(contour_point_list == point1, axis=1))[0]
    idx2 = np.where(np.all(contour_point_list == point2, axis=1))[0]

    if len(idx1) == 0 or len(idx2) == 0:
        raise ValueError("One or both points are not found in the contour.")

    # Find indices of point1 and point2 in the contour
    idx1 = idx1[0]  # First occurrence of point1
    idx2 = idx2[0]  # First occurrence of point2

    # Slice contour depending on the relative positions of idx1 and idx2
    if idx2 < idx1:
        # If point2 comes before point1, slice from point2 to the end, and then from start to point1
        sliced_contour = np.concatenate([contour_point_list[idx1:], contour_point_list[:idx2]])
    else:
        # Otherwise, slice from point2 to point1
        sliced_contour = contour_point_list[idx1:idx2]

    return sliced_contour


def insert_points_into_contour(sliced_contour, new_points, position="end"):
    """
    Inserts new points into the sliced contour.
    position: 'start' to insert at the beginning, 'end' to insert at the end.
    """
    if position == "start":
        # Insert at the beginning of the sliced contour
        new_contour = np.vstack([new_points, sliced_contour])
    elif position == "end":
        # Insert at the end of the sliced contour
        new_contour = np.vstack([sliced_contour, new_points])
    else:
        raise ValueError("Position must be either 'start' or 'end'.")

    return new_contour


def vector_angle(point1, point2):
    vector = (point2[0] - point1[0], point2[1] - point1[1])
    vector_angle = cv2.fastAtan2(vector[0], vector[1])
    return vector_angle


def dynamic_resize_image_to_target(input_image, size, fill_color):
    """
    Resizes the input image to fit within the target resolution, maintaining its aspect ratio.
    The resized image is then placed on a square canvas, with the lower part of the image aligned
    to the bottom of the canvas. The remaining space is filled with the specified background color.

    Parameters:
    - input_image: The image to resize (should be a NumPy array).
    - size: The target resolution size for the square canvas (e.g., 224).
    - fill_color: The background color (as a tuple of (B, G, R)) to fill the empty space.

    Returns:
    - new_image: The new image with the resized input image placed on a square canvas.
    """
    # Get the original image dimensions (height and width)
    original_height, original_width = input_image.shape[:2]

    # Determine scaling factor based on the larger dimension
    if original_width > original_height:
        new_width = size
        new_height = int(original_height * (size / original_width))
    else:
        new_height = size
        new_width = int(original_width * (size / original_height))

    # Resize the input image using OpenCV
    resized_image = cv2.resize(input_image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    # Create a new square image with the background color
    new_image = np.full((size, size, 3), fill_color, dtype=np.uint8)  # Background filled with the specified color

    # Calculate the position for placing the resized image in the new square canvas
    top_left_x = (size - new_width) // 2  # Centering horizontally
    top_left_y = size - new_height  # Aligning the bottom of the image with the bottom of the square canvas

    # Copy the resized image onto the new square canvas
    new_image[top_left_y : top_left_y + new_height, top_left_x : top_left_x + new_width] = resized_image

    return new_image


# Display all images in an array of images
def show_images(images):
    for image in images:
        cv2.imshow("Images", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Create a binary handmask with HSV values
def create_handmask(original_image):
    # Apply gaussian filter
    blurred_image = cv2.GaussianBlur(original_image, (11, 11), 2)

    # Define the range for skin color in HSV(Hue, Saturation, Value)
    # These values might need to be adjusted depending on lighting and skin tone
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 40, 80])  # Lower bound of skin color (Hue, Saturation, Value)
    upper_skin = np.array([20, 255, 255])  # Upper bound of skin color

    # Create a mask for the skin color
    hand_mask = cv2.inRange(hsv, lower_skin, upper_skin)

    return hand_mask


def detect_largest_defects(largest_contour):
    # Find the convex hull of the largest contour
    hull = cv2.convexHull(largest_contour, returnPoints=False)

    # Find the convexity defects
    defects = cv2.convexityDefects(largest_contour, hull)

    defect_distances = []
    for i in range(defects.shape[0]):
        # Extract defect details
        start_idx, end_idx, farthest_idx, defect_distance = defects[i, 0]
        farthest_point = tuple(largest_contour[farthest_idx][0])

        defect_distances.append([defect_distance, farthest_point])

    defect_distances.sort(reverse=True)
    four_largest_defects = []
    for i in range(4):
        four_largest_defects.append(defect_distances[i][1])

    return four_largest_defects


def detect_missing_point(first_defect, second_defect, contour_mask, blank_image):
    direction_vector = find_direction_vector(first_defect, second_defect)
    moved_point = (int(first_defect[0] + direction_vector[0] * 3), int(second_defect[1] + direction_vector[1] * 3))

    line_mask = blank_image.copy()
    line_mask = cv2.line(line_mask, first_defect, moved_point, 255, 1)
    intersections = cv2.bitwise_and(contour_mask, line_mask)
    swapped_intersection_points = np.column_stack(np.where(intersections == 255))

    intersection_points = [(x, y) for y, x in swapped_intersection_points]
    detected_point = find_closest_point(intersection_points, moved_point)

    return detected_point


def count_white_pixels(image):
    return np.sum(image == 255)


def draw_images_in_grid(image_list, rows, cols, image_size=(224, 224), padding=10, bg_color=(13, 17, 23)):
    """
    Draw an array of images on a single canvas.

    Parameters:
    - image_list: List of image arrays (NumPy arrays).
    - rows: Number of rows in the grid.
    - cols: Number of columns in the grid.
    - image_size: Tuple specifying the size (width, height) to resize each image.
    - padding: Padding between images in pixels.
    - bg_color: Background color as a BGR tuple (default is white).
    """
    # Calculate the size of the canvas
    canvas_height = rows * (image_size[1] + padding) + padding
    canvas_width = cols * (image_size[0] + padding) + padding

    # Create a blank canvas with the background color
    canvas = np.full((canvas_height, canvas_width, 3), bg_color, dtype=np.uint8)

    # Loop through images and place them on the canvas
    for i, img in enumerate(image_list):
        if i >= rows * cols:
            break  # Avoid adding more images than the grid can hold
        # Convert grayscale to color if necessary
        if len(img.shape) == 2:  # Check if image is grayscale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # Resize the image to the specified size
        img_resized = cv2.resize(img, image_size)

        # Calculate position to place the image
        row = i // cols
        col = i % cols
        y = padding + row * (image_size[1] + padding)
        x = padding + col * (image_size[0] + padding)

        # Place the resized image on the canvas
        canvas[y : y + image_size[1], x : x + image_size[0]] = img_resized

    return canvas
