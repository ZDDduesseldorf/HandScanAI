import cv2
import numpy as np


def calculate_image_metrics(image_path):
    """
    calculates brightness (mean), contrast (standard_devitaion) and sharpness (variance_of_laplacian) of the image

    :param image_path: name of the image

    return: mean, standard_devitatiion, variance_of_laplacian
    """
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = np.mean(gray)
    standard_deviation = np.std(gray)
    variance_of_laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    return mean, standard_deviation, variance_of_laplacian
