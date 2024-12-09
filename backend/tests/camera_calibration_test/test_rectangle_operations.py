import pytest
import numpy as np
from camera_calibration.rectangle_operations import *


def test_remove_close_points():
    points = np.array([[0, 0], [1, 1], [2, 2], [10, 10]])
    filtered_points = remove_close_points(points, max_distance=3)
    expected_filtered_points = np.array([[0, 0], [10, 10]])
    np.testing.assert_array_equal(filtered_points, expected_filtered_points)

def test_remove_outer_clips():
    rectangle = np.array([[[1039, 1170]], [[1063, 1367]], [[1219, 1153]], [[1244, 1351]]])
    clipped_rectangle = remove_outer_clips(rectangle)
    expected_clipped_rectangle = np.array([[1039, 1170], [1063, 1367], [1219, 1153], [1244, 1351]])
    np.testing.assert_array_equal(clipped_rectangle, expected_clipped_rectangle)

def test_sort_points():
    rectangle = np.array([[[1039, 1170]], [[1063, 1367]], [[1219, 1153]], [[1244, 1351]]])
    sorted_rectangle = sort_points(rectangle)
    expected_sorted_rectangle = np.array([[1039, 1170], [1063, 1367], [1219, 1153], [1244, 1351]])
    np.testing.assert_array_equal(sorted_rectangle, expected_sorted_rectangle)

def test_distance():
    p1 = np.array([0, 0])
    p2 = np.array([3, 4])
    dist = distance(p1, p2)
    expected_dist = 5.0  # Pythagoras: sqrt(3^2 + 4^2)
    assert np.isclose(dist, expected_dist)

def test_calculate_extensive():
    rectangle = np.array([[[0, 0]],[[0, 1]], [[1, 1]], [[1, 0]]])
    extensive = calculate_extensive(rectangle)
    
    print(f"{extensive}")
    # Berechne den Umfang manuell: 
    point1 = [0, 0]
    point2 = [0, 1]
    point3 = [1, 1]
    point4 = [1, 0]
    
    dist1 = distance(point1, point2)
    dist2 = distance(point2, point3)
    dist3 = distance(point3, point4)
    dist4 = distance(point4, point1)
    
    expected_extensive = dist1 + dist2 + dist3 + dist4
    assert np.isclose(extensive, expected_extensive)

def test_find_rectangle_failes():
    image_path = "tests/data/calibration/no_rectangle.jpg"
    with pytest.raises(ValueError, match="kein Rechteck gefunden"):
        find_rectangle(image_path)

def test_find_rectangle():
    image_path = "tests/data/calibration/kali_test.jpg"
    rectangle = find_rectangle(image_path)

    assert len(rectangle) == 4
    