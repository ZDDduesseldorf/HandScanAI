from camera_calibration import rectangle_operations
from camera_calibration import image_operations


def create_calibration_file(image_path: str, file_name: str, detected_rectangle: bool = False):
    """
    creates a file that includes all calibrationvalues: mean, standard_deviation, variance_of_laplacian,
    extensive, Point1-4 (x y)

    Args:
        image_path (str): path to image
        file_name (str): path to calibration-file
        detected_rectangle (bool, optional): Flag for wheter or not using rectangle detection. Defaults to False.
    """

    f1 = open(file_name, "w")
    metrics = image_operations.calculate_image_metrics(image_path)

    f1.write(str(metrics[0]) + "\n" + str(metrics[1]) + "\n" + (str(metrics[2]) + "\n"))

    # only when there is a rectangle to detect
    if detected_rectangle:
        extensive, sorted_rectangle = rectangle_operations.rectangle_operations_calibration_file(image_path)
        f1.write(str(extensive) + "\n")

        for point in sorted_rectangle:
            f1.write(f"{point[0]} {point[1]}\n")

    f1.close()


# when all are true calibration succseeded


def check_kalibration(image_path: str, file_name: str, detected_rectangle: bool = False):
    """
    checks the calibration by comparing the values of the current image with those in the calibration file

    Args:
        image_path (str): path to image
        file_name (str): path to calibration-file
        detected_rectangle (bool, optional): Flag for wheter or not using rectangle detection. Defaults to False.

    Returns:
        bool: True when calibration is successful, False if calibration failed
    """

    k_values = read_calibrationfile(file_name, detected_rectangle)
    metrics = image_operations.calculate_image_metrics(image_path)

    # detect rectangle
    rectangle = None
    if detected_rectangle:
        rectangle = rectangle_operations.find_rectangle(image_path)
        if (
            compare_mean(metrics, k_values)
            and compare_std(metrics, k_values)
            and compare_sharpness(metrics, k_values)
            and compare_extensive(rectangle, k_values)
            and compare_rectangle(rectangle, k_values)
        ):
            print("Kalibrierung erfolgreich")
            return True
        else:
            return False
    else:
        if compare_mean(metrics, k_values) and compare_std(metrics, k_values) and compare_sharpness(metrics, k_values):
            print(metrics, k_values)
            return True
        else:
            return False


###############################################
# helper functions


def read_calibrationfile(file_name: str, detected_rectangle: bool = False):
    """reads the calbrationfile and save values as variables

    Args:
        file_name (str): path to calibration-file
        detected_rectangle (bool, optional): Flag for wheter or not using rectangle detection. Defaults to False.

    Returns:
        list: list with all values in this shape [mean, standard_devitation, variance_of_laplacian, extensive,
    [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]]
    """

    k_rectangle = []
    with open(file_name) as file:
        rows = file.readlines()

    if len(rows) <= 8:
        k_mean = rows[0].strip()
        k_mean = float(k_mean)
        k_standard_deviation = rows[1].strip()
        k_standard_deviation = float(k_standard_deviation)
        k_variance_of_laplacian = rows[2].strip()
        k_variance_of_laplacian = float(k_variance_of_laplacian)

    if detected_rectangle:
        k_extensive = rows[3].strip()
        k_extensive = float(k_extensive)
        for line in rows[4:]:
            point_x, point_y = line.strip().split(" ")
            point_x = int(point_x)
            point_y = int(point_y)
            k_rectangle.append([point_x, point_y])
        return [k_mean, k_standard_deviation, k_variance_of_laplacian, k_extensive, k_rectangle]

    return [k_mean, k_standard_deviation, k_variance_of_laplacian]


def compare_mean(metrics: list, k_values: list):
    """
    compares the mean of the actual image and the value from the calibration file

    Args:
        metrics (list): list of values from actual image
        k_values (list): list of values from calibration file

    Raises:
        ValueError: image is too bright
        ValueError: image is too dark

    Returns:
        bool: True, when differnce is smaller than threshold
    """

    mean = metrics[0]
    k_mean = k_values[0]
    th = 5
    # compare mean
    if abs(mean - k_mean) < th:
        return True
    elif (mean - k_mean) > th:
        raise ValueError("Bild ist zu hell")
    elif (mean - k_mean) < -th:
        raise ValueError("Bild ist zu dunkel")


def compare_std(metrics: list, k_values: list):
    """compares the standard_devitation of the actual image and the value from the calibration file

    Args:
        metrics (list): list of values from actual image
        k_values (list): list of values from calibration file

    Raises:
        ValueError: contrast is too big
        ValueError: contrast is too small

    Returns:
        bool: True, when differnce is smaller than threshold
    """

    standard_deviation = metrics[1]
    k_standard_deviation = k_values[1]
    th = 5
    # compare standard_deviation
    if abs(standard_deviation - k_standard_deviation) < th:
        return True
    elif (standard_deviation - k_standard_deviation) > th:
        raise ValueError("Kontrast ist zu groß")
    elif (standard_deviation - k_standard_deviation) < -th:
        raise ValueError("Kontrast ist zu klein")


def compare_sharpness(metrics: list, k_values: list):
    """compares the sharpness of the actual image and the value from the calibration file

    Args:
        metrics (list): list of values from actual image
        k_values (list): list of values from calibration file

    Raises:
        ValueError: Image is too blurred

    Returns:
        bool: True, when differnce is smaller than threshold
    """

    variance_of_laplacian = metrics[2]
    k_variance_of_laplacian = k_values[2]
    th = 1
    # compare sharpness
    if abs(variance_of_laplacian - k_variance_of_laplacian) <= th:
        return True
    elif (variance_of_laplacian - k_variance_of_laplacian) > th:
        return True
    else:
        raise ValueError("Bild ist zu unscharf")


def compare_rectangle(rectangle: list, k_values: list):
    """compares the points of the rectangle of the actual image and from the calibration file

    Args:
        rectangle (list): list of points of the rectangle from actual image
        k_values (list): list of values from calibration file

    Raises:
        ValueError: when one point is out of threshold

    Returns:
        bool: True, when all points are in the threshold
    """

    sort_rectangle = rectangle_operations.sort_points(rectangle)

    k_rectangle = k_values[4]
    index = 0
    threshold = 100
    for point, k_point in zip(sort_rectangle, k_rectangle):
        if (abs(point[0] - k_point[0]) < threshold) and (abs(point[1] - k_point[1]) < threshold):
            index += 1
        else:
            raise ValueError(f"Rechtecke nicht identisch bei Punkt {point}")

    if index == 4:
        return True


def compare_extensive(rectangle: list, k_values: list):
    """compares the extensive of the actual image and the value from the calibration file

    Args:
        rectangle (list): list of points of the rectangle from actual image
        k_values (list): list of values from calibration file

    Raises:
        ValueError: rectangle too small
        ValueError: rectangle too big

    Returns:
        bool: True, when differnce is smaller than threshold
    """

    extensive = rectangle_operations.calculate_extensive(rectangle)
    print(f"{extensive}")
    k_extensive = k_values[3]

    difference = abs(k_extensive - extensive) / k_extensive
    if difference < 0.1:
        return True
    else:
        if extensive > k_extensive:
            raise ValueError("Rechteck zu groß")
        else:
            raise ValueError("Rechteck zu klein")
