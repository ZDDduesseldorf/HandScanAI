import cv2
import numpy as np


def rectangle_operations_calibration_file(image_path: str):
    """
    Dectects a rectangle in the image, sorts the points and calculate the extensive

    Args:
        image_path (str): path to image

    Returns:
        extensive (float), sorted_rectangle(list)
    """
    rectangle = find_rectangle(image_path)
    sorted_rectangle = sort_points(rectangle)
    extensive = calculate_extensive(rectangle)

    return extensive, sorted_rectangle


def find_rectangle(image_path: str):
    """detects a rectangle in the image with Canny Edge-detection and contourfinder

    Args:
        image_path (str): path to image

    Raises:
        ValueError: if no rectangle is detected

    Returns:
        list:  list with the four corner points of the rectangle
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


def remove_close_points(points: list, max_distance: int = 50):
    """Removes points that are closer than a specified maximum distance to any other point in the list.

    Args:
        points (list): numpy array of shape (N, 2) representing a list of points in 2D space.
        max_distance (int, optional): Maximum allowed distance between two points. Points closer than
                         this distance to an existing point in the filtered list will be removed. Defaults to 50.

    Returns:
        numpy array : iltered points where no two points are closer than `max_distance`.
    """

    filtered = []
    for p in points:
        if not any(np.linalg.norm(p - f) < max_distance for f in filtered):
            filtered.append(p)
    return np.array(filtered)


def remove_outer_clips(rectangle: list):
    """Removes the outer dimension of a given rectangle array, simplifying its shape.

    Args:
        rectangle (list): numpy array of shape (N, 1, 2) representing a list
                      of points in 2D space.

    Returns:
        list: reshaped rectangle
    """

    return rectangle.reshape(-1, 2)


def sort_points(rectangle: list):
    """Sorts the points of a rectangle by their x-coordinate values in ascending order.

    Args:
        rectangle (list): numpy array of shape (N, 1, 2) representing a list
                      of points in 2D space.

    Returns:
        numpy array: shape (N, 2) with points sorted by their x-values in ascending order.
    """

    rectangle_cutted = remove_outer_clips(rectangle)
    return rectangle_cutted[rectangle_cutted[:, 0].argsort()]


def distance(p1: tuple, p2: tuple):
    """Calculates the Euclidean distance between two points in 2D space.

    Args:
        p1 (tuple): A tuple  representing the points (x1, y1)
        p2 (tuple): A tuple  representing the points (x2, y2)

    Returns:
        float: The Euclidean distance as a float.
    """

    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def calculate_extensive(rectangle: list):
    """Calculates the extensive property of a rectangle, which is the total perimeter
    or cumulative distance of its edges.


    Args:
        rectangle (list): numpy array of shape (N, 1, 2) representing the
                      points of a rectangle in 2D space.

    Returns:
        float: The extensive value (total perimeter) as a float.
    """

    extensive = 0
    rectangle_cutted = remove_outer_clips(rectangle)
    for i in range(len(rectangle_cutted)):
        point1 = rectangle_cutted[i]
        point2 = rectangle_cutted[(i + 1) % len(rectangle)]
        extensive += distance(point1, point2)

    return extensive
