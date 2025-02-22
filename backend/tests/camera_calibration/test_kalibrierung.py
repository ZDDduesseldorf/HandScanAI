import pytest
import numpy as np

import camera_calibration.kalibrierung as kali


@pytest.fixture()
def setup_method():
    image_path = "tests/data/calibration/kali_test.jpg"
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    kali.create_calibration_file(image_path, file_name, detected_rectangle=False)
    print("Setup abgeschlossen")


def test_compare_mean_within_threshold():
    metrics = [100, 112, 98]
    k_values = [99, 101, 97]
    assert kali.compare_mean(metrics, k_values)


def test_compare_mean_too_bright():
    metrics = [110, 112, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Bild ist zu hell"):
        kali.compare_mean(metrics, k_values)


def test_compare_mean_too_dark():
    metrics = [90, 112, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Bild ist zu dunkel"):
        kali.compare_mean(metrics, k_values)


def test_compare_std_within_threshold():
    metrics = [100, 102, 98]
    k_values = [99, 101, 97]
    assert kali.compare_std(metrics, k_values)


def test_compare_std_too_high():
    metrics = [100, 107, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Kontrast ist zu groß"):
        kali.compare_std(metrics, k_values)


def test_compare_std_too_low():
    metrics = [100, 95, 98]
    k_values = [99, 101, 97]
    with pytest.raises(ValueError, match="Kontrast ist zu klein"):
        kali.compare_std(metrics, k_values)


def test_compare_sharpness_within_threshold():
    metrics = [100, 102, 10]
    k_values = [99, 101, 9]
    assert kali.compare_sharpness(metrics, k_values)


def test_compare_sharpness_too_low():
    metrics = [100, 112, 7]
    k_values = [99, 101, 9]
    with pytest.raises(ValueError, match="Bild ist zu unscharf"):
        kali.compare_sharpness(metrics, k_values)


def test_compare_rectangle_identical():
    rectangle = [[1009, 1130]], [[1093, 1347]], [[1209, 1183]], [[1234, 1391]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 760, [[1039, 1170], [1063, 1367], [1219, 1153], [1244, 1351]]]
    assert kali.compare_rectangle(rectangle, k_values)


def test_compare_rectangle_not_identical():
    rectangle = [[909, 1130]], [[1093, 1347]], [[1209, 1183]], [[1234, 1391]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 760, [[1039, 1170], [1063, 1367], [1219, 1153], [1244, 1351]]]
    with pytest.raises(ValueError, match=r"Rechtecke nicht identisch bei Punkt \[ *909 1130\]"):
        kali.compare_rectangle(rectangle, k_values)


def test_compare_extensive_within_threshold():
    rectangle = [[0, 0], [0, 1], [1, 1], [1, 0]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 4, [[0, 0], [0, 1], [1, 1], [1, 0]]]
    assert kali.compare_extensive(rectangle, k_values)


def test_compare_extensive_too_high():
    rectangle = [[0, 0], [0, 2], [2, 2], [2, 0]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 4, [[0, 0], [0, 1], [1, 1], [1, 0]]]
    with pytest.raises(ValueError, match="Rechteck zu groß"):
        kali.compare_extensive(rectangle, k_values)


def test_compare_extensive_too_low():
    rectangle = [[0, 0], [0, 0.5], [0.5, 0.5], [0.5, 0]]
    rectangle = np.array(rectangle)
    k_values = [99, 101, 9, 4, [[0, 0], [0, 1], [1, 1], [1, 0]]]
    with pytest.raises(ValueError, match="Rechteck zu klein"):
        kali.compare_extensive(rectangle, k_values)


def test_check_kali(setup_method):
    image_path = "tests/data/calibration/kali_test.jpg"
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    assert kali.check_kalibration(image_path, file_name, detected_rectangle=False)


def test_check_kali_failes(setup_method):
    image_path = "tests/data/calibration/failed_kali.jpg"
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    with pytest.raises(ValueError):
        kali.check_kalibration(image_path, file_name)


def test_read_calibration_file(setup_method):
    detected_rectangle = False
    file_name = "tests/data/calibration/kalibrierungswerte.txt"
    k_values = kali.read_calibrationfile(file_name, detected_rectangle)
    if detected_rectangle:
        expected_values = (
            250.616159456983,
            20.653294995518543,
            0.8325489485543115,
            996.1001768764597,
            [[1913, 995], [1917, 1246], [2160, 992], [2164, 1243]],
        )
    else:
        expected_values = (
            250.616159456983,
            20.653294995518543,
            0.8325489485543115,
        )

    # Vergleiche die numerischen Werte zuerst
    for i in range(3):
        assert np.isclose(k_values[i], expected_values[i]), f"Mismatch in value {i}"

    if detected_rectangle:
        assert np.isclose(k_values[3], expected_values[3])
        # Vergleiche die 2D-Listen
        for i in range(4, len(k_values)):
            np.testing.assert_array_equal(k_values[i], expected_values[i])
