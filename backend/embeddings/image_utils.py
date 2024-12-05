import os
from torchvision.io import read_image, ImageReadMode


def load_image(image_name, path_to_images):
    """
    Loads image from from image name and general path to the image folder.

    Args:
        image_name: name of the individual image-file
        path_to_images: path to the image folder, where the image lies

    Returns:
        A 3 dimensional RGB Tensor of the image. The values of the output tensor are uint8 in [0, 255].
    """
    img_path = construct_image_path(image_name, path_to_images)

    # Read the image file
    image_tensor = read_image(img_path, ImageReadMode.RGB)
    # returns a tensor with rgb values
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
