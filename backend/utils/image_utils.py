import os
import cv2
import shutil


def copy_image_to_folder(uuid, original_folder_path, target_folder_path):
    image_name = uuid + ".jpg"
    original = construct_image_path(image_name, original_folder_path)
    target = construct_image_path(image_name, target_folder_path)
    try:
        shutil.copy(original, target)
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


def load_image_from_full_path(path_to_image):
    """
    Loads image from from image name and general path to the image folder.

    Args:
        path_to_image: full path to the image

    Returns:
        A 3 dimensional RGB numpy array of the image. The values of the output tensor are uint8 in [0, 255].
    """
    # Read the image file
    image_tensor = cv2.imread(path_to_image)
    image_tensor = cv2.cvtColor(image_tensor, cv2.COLOR_BGR2RGB)
    # returns a tensor with rgb values
    return image_tensor


def load_image_from_path_fragments(image_name, path_to_images):
    """
    Loads image from from image name and general path to the image folder.

    Args:
        image_name: name of the individual image-file
        path_to_images: path to the image folder, where the image lies

    Returns:
        A 3 dimensional RGB numpy array of the image. The values of the output tensor are uint8 in [0, 255].
    """
    img_path = construct_image_path(image_name, path_to_images)

    # Read the image file
    image_tensor = load_image_from_full_path(img_path)
    # returns a numpy array with rgb values
    return image_tensor


def construct_image_path(image_name, path_to_images):
    """
    Helper function: Constructs individual image path from image name and general path to the image folder.

    Args:
        image_name: name of the individual image-file
        path_to_images: path to the image folder, where the image lies

    Returns:
        A string, the path to the input image from where it can be loaded.
    """
    # Construct the full path to the image file
    img_path = os.path.join(path_to_images, image_name)
    return img_path


def get_image_path(folder_path_query, uuid):
    """
    Finds and returns the file path to an image based on its UUID and supported extensions.

    Args:
        temp_base_dir (Path): The base directory. Typically derived from the current file's location.
        uuid (str): Unique identifier for the image

    Returns:
        Path: The absolute path to the image file if found.
        None: If no file with the given UUID and extensions exists in the specified folder.
    """
    extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    for ext in extensions:
        image_path = folder_path_query / f"{uuid}{ext}"
        if image_path.exists():
            return image_path.resolve()
    return None
