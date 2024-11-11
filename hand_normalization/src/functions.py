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