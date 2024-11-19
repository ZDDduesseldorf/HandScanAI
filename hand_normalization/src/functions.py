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
                    # Get landmark name from mp_hands.HandLandmark
                    landmark_name = mp_hands.HandLandmark(idx).name
                    
                    # Get the coordinates in image dimensions
                    h, w, _ = image.shape  # Get image dimensions
                    x, y = int(landmark.x * w), int(landmark.y * h)  # Scale x, y to image dimensions

                    output.append([landmark_name, x, y])
    return output

# Function to calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)**(0.5)

def direction_vector(point1, point2):
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
    return sort_points_by_closeness(array_of_points,given_point)[0]

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

def rotate_image_no_crop(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    
    # Calculate the new bounding dimensions of the image
    cos = abs(rotation_matrix[0, 0])
    sin = abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # Adjust the rotation matrix to account for translation
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]
    
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))
    
    return rotated_image


def check_points_in_mask(mask, points):
    # Create a blank canvas (black image) of the same size as the mask
    canvas = np.zeros_like(mask, dtype=np.uint8)
    
    # List to store the points that are inside the mask
    inside_points = []
    
    for point in points:
        # Draw the point on the canvas (white pixel)
        cv2.circle(canvas, point, 1, (255), -1)  # Draw a small white dot at the point
        
        # Check if the mask has a non-zero value at this point
        if mask[point[1], point[0]] > 0:  # Use (x, y) for the index
            inside_points.append(point)
    
    return inside_points

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

def insert_points_into_contour(sliced_contour, new_points, position='end'):
    """
    Inserts new points into the sliced contour.
    position: 'start' to insert at the beginning, 'end' to insert at the end.
    """
    if position == 'start':
        # Insert at the beginning of the sliced contour
        new_contour = np.vstack([new_points, sliced_contour])
    elif position == 'end':
        # Insert at the end of the sliced contour
        new_contour = np.vstack([sliced_contour, new_points])
    else:
        raise ValueError("Position must be either 'start' or 'end'.")

    return new_contour

def vector_agle(point1, point2):
    vector = (point1[1] - point2[1] , point1[2] - point2[2])
    vector_angle = cv2.fastAtan2(vector[0],vector[1]) + 90