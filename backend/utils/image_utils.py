import os
import cv2
import shutil
from pathlib import Path


def copy_image_to_folder(uuid: str, original_folder_path: (str | Path), target_folder_path: (str | Path)):
    """
    Copies an image from one folder to another.

    Args:
        uuid (str): uuid of the image to be copied
        original_folder_path (str | Path): full path to the folder where the image lies
        target_folder_path (str | Path): full path to the folder where the image should be copied to

    Returns:
        bool: Returns true if copying the file was successfull
    """
    image_name = uuid + ".jpg"
    original = construct_image_path(image_name, original_folder_path)
    target = construct_image_path(image_name, target_folder_path)
    return save_image_under_new_path(original, target)


def save_image_under_new_path(original_image_path: (str | Path), target_image_path: (str | Path)):
    """
    Copies an image from one path to another path.

    Args:
        original_image_path (str | Path): full path to original imagefile
        target_image_path (str | Path): full path to new imagefile

    Returns:
        success (bool): Returns true if copying the file was successfull
    """
    try:
        shutil.copy(original_image_path, target_image_path)
        print("File copied successfully.")
        return True
        # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
        return False
        # If there is any permission issue
    except PermissionError:
        print("Permission denied.")
        return False


def load_image_from_full_path(path_to_image: (str | Path)):
    """
    Loads image from absolut image path into a numpy array.

    Args:
        path_to_image (str | Path): absolute path to the image

    Returns:
        image_tensor (ndarray): A 3 dimensional RGB numpy array of the image. The values are uint8 in [0, 255].
    """
    # Read the image file
    image_tensor = cv2.imread(path_to_image)
    image_tensor = cv2.cvtColor(image_tensor, cv2.COLOR_BGR2RGB)
    # returns a ndarray with rgb values
    return image_tensor


def load_image_from_path_fragments(image_name: str, path_to_images: (str | Path)):
    """
    Loads image from a given image name and the path to the image folder.

    Args:
        image_name (str): name of the individual image-file
        path_to_images (str | Path): path to the folder that contains the image

    Returns:
        image_tensor (ndarray): A 3 dimensional RGB numpy array of the image. The values are uint8 in [0, 255].
    """
    img_path = construct_image_path(image_name, path_to_images)

    # Read the image file
    image_tensor = load_image_from_full_path(img_path)
    # returns a numpy array with rgb values
    return image_tensor


def construct_image_path(image_name: str, path_to_images: (str | Path)):
    """
    Helper function: Constructs an absolute path from a folder path and an image name.

    Args:
        image_name (str): name of the individual image-file
        path_to_images (str | Path): path to the folder that contains the image

    Returns:
        img_path (str): The absolute path to an image-file.
    """
    # Construct the full path to the image file
    img_path = os.path.join(path_to_images, image_name)
    return img_path


def get_image_path(folder_path_query: Path, uuid: str):
    """
    Finds and returns the file path to an image based on its UUID and supported extensions.

    Args:
        temp_base_dir (Path): The base directory. Typically derived from the current file's location.
        uuid (str): Unique identifier for the image

    Returns:
        out (Path | None): Returns either the absolute path to the image file if found. OR returns None if no file with the given UUID and extensions exists in the specified folder.
    """
    extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    for ext in extensions:
        image_path = folder_path_query / f"{uuid}{ext}"
        if image_path.exists():
            return image_path.resolve()
    return None
