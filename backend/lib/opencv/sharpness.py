import cv2


def calculate_sharpness(image: cv2.imread) -> float:
    """Calculate the sharpness of an image using the Laplacian variance method"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var
