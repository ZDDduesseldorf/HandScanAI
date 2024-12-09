import pytest
import numpy as np
import os

from camera_calibration.kalibrierung import *



def test_compare_mean_within_threshold():
    metrics = [100, 112, 98]
    k_values = [99, 101, 97]
    assert compare_mean(metrics, k_values) == True

def test_compare_mean_too_bright():
    metrics = [110, 112, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Bild ist zu hell"):
       compare_mean(metrics, k_values)

def test_compare_mean_too_dark():
    metrics = [90, 112, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Bild ist zu dunkel"):
        compare_mean(metrics, k_values)


def test_compare_std_within_threshold():
    metrics = [100, 102, 98]
    k_values = [99, 101, 97]
    assert compare_std(metrics, k_values) == True

def test_compare_std_too_high():
    metrics = [100, 107, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Kontrast ist zu groß"):
       compare_std(metrics, k_values)

def test_compare_std_too_low():
    metrics = [100, 95, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Kontrast ist zu klein"):
        compare_std(metrics, k_values)


def test_compare_sharpness_within_threshold():
    metrics = [100, 102, 10]
    k_values = [99, 101, 9]
    assert compare_sharpness(metrics, k_values) == True

def test_compare_sharpness_too_low():
    metrics = [100, 112, 7]
    k_values = [99, 101, 9]
    with pytest.raises(ValueError, match="Bild ist zu unscharf"):
        compare_sharpness(metrics, k_values)


def test_compare_rectangle_identical():
    rectangle = [[1009, 1130]],[[1093, 1347]], [[1209, 1183]], [[1234, 1391]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 760, [[1039, 1170],[1063, 1367], [1219, 1153], [1244, 1351]]]
    assert compare_rectangle(rectangle, k_values) == True

def test_compare_rectangle_not_identical():
    rectangle = [[909, 1130]],[[1093, 1347]], [[1209, 1183]], [[1234, 1391]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 760, [[1039, 1170],[1063, 1367], [1219, 1153], [1244, 1351]]]
    with pytest.raises(ValueError, match=r"Rechtecke nicht identisch bei Punkt \[ *909 1130\]"):
        compare_rectangle(rectangle, k_values)


def test_compare_extensive_within_threshold():
    rectangle = [[0, 0],[0, 1], [1, 1], [1, 0]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 4, [[0, 0],[0, 1], [1, 1], [1, 0]]]
    assert compare_extensive(rectangle, k_values) == True

def test_compare_extensive_too_high():
    rectangle = [[0, 0],[0, 2], [2, 2], [2, 0]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 4, [[0, 0],[0, 1], [1, 1], [1, 0]]]
    with pytest.raises(ValueError, match="Rechteck zu groß"):
       compare_extensive(rectangle, k_values)

def test_compare_extensive_too_low():
    rectangle = [[0, 0],[0, 0.5], [0.5,0.5], [0.5, 0]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 4, [[0, 0],[0, 1], [1, 1], [1, 0]]]
    with pytest.raises(ValueError, match="Rechteck zu klein"):
        compare_extensive(rectangle, k_values)


def test_check_kali():
    image_path = "tests/data/calibration/kali_test.jpg"
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    assert check_kalibration(image_path, file_name) == True

def test_check_kali_failes():
    image_path = "tests/data/calibration/failed_kali.jpg"
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    with pytest.raises(ValueError): 
        check_kalibration(image_path, file_name) == False


def test_read_calibration_file():
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    k_values = read_calibrationfile(file_name)
    expected_values = (233.9558369502315, 60.45824616558628, 9.971898990259211, 760.5353882456766, [[1039, 1170], [1063, 1367], [1219, 1153], [1244, 1351]])
    print(k_values)
    # Vergleiche die numerischen Werte zuerst
    for i in range(4):
        assert np.isclose(k_values[i], expected_values[i]), f"Mismatch in value {i}"

    # Vergleiche die 2D-Listen
    for i in range(4, len(k_values)):
        np.testing.assert_array_equal(k_values[i], expected_values[i])