import cv2
import numpy as np


<<<<<<< HEAD
def rectangle_operations_calibration_file(image_path):
    rectangle = find_rectangle(image_path)
    sorted_rectangle = sort_points(rectangle)
    extensive = calculate_extensive(rectangle)

    return extensive, sorted_rectangle


=======
>>>>>>> 8b832e548096a4e4d0fa44eb47c9225cef3d8034
def find_rectangle(image_path):
    """
    detects a rectangle in the image with Canny Edge-detection and contourfinder

    :param image_path: name of the image

    return: list with the four corner points of the rectangle
    raise ValueError: if no rectangle is detected
    """
    # load image
    image = cv2.imread(image_path)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Smoothing to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # simplify contour and remove close points so that only 4 corner points remain
    # return rectangle with 4 points
    for contour in contours:
        epsilon = max(0.02 * cv2.arcLength(contour, True), 1.0)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        approx = remove_close_points(approx[:, 0], max_distance=50)
        approx = approx.reshape(-1, 1, 2)

        if len(approx) == 4:
            return approx

    raise ValueError("kein Rechteck gefunden")


###############################################
# helper functions


def remove_close_points(points, max_distance=50):
    """
    Removes points that are closer than a specified maximum distance to any other point in the list.

    :param points: numpy array of shape (N, 2) representing a list of points in 2D space.
    :param max_distance: Maximum allowed distance between two points. Points closer than
                         this distance to an existing point in the filtered list will be removed.
                         Default is 50 pixels.

    return: numpy array of filtered points where no two points are closer than `max_distance`.
    """
    filtered = []
    for p in points:
        if not any(np.linalg.norm(p - f) < max_distance for f in filtered):
            filtered.append(p)
    return np.array(filtered)


def remove_outer_clips(rectangle):
    """
    Removes the outer dimension of a given rectangle array, simplifying its shape.
    """
    return rectangle.reshape(-1, 2)


def sort_points(rectangle):
    """
    Sorts the points of a rectangle by their x-coordinate values in ascending order.

    :param rectangle: numpy array of shape (N, 1, 2) representing a list
                      of points in 2D space.

    :return: numpy array of shape (N, 2) with points sorted by their x-values in ascending order.
    """
    rectangle_cutted = remove_outer_clips(rectangle)
    return rectangle_cutted[rectangle_cutted[:, 0].argsort()]


def distance(p1, p2):
    """
    Calculates the Euclidean distance between two points in 2D space.

    :param p1, p2: A tuple  representing the points (x1, y1).

    :return: The Euclidean distance as a float.
    """
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def calculate_extensive(rectangle):
    """
    Calculates the extensive property of a rectangle, which is the total perimeter
    or cumulative distance of its edges.

    :param rectangle: numpy array of shape (N, 1, 2) representing the
                      points of a rectangle in 2D space.

    :return: The extensive value (total perimeter) as a float.
    """
    extensive = 0
    rectangle_cutted = remove_outer_clips(rectangle)
    for i in range(len(rectangle_cutted)):
        point1 = rectangle_cutted[i]
        point2 = rectangle_cutted[(i + 1) % len(rectangle)]
        extensive += distance(point1, point2)

    return extensive


rectangle = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
print(f"Umfang des Rechtecks: {calculate_extensive(rectangle)}")
