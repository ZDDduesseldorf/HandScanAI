import os

from utils import image_utils
from pathlib import Path


### TESTS #############################################################


def test_load_image_from_fragments(image_name, path_to_images):
    loaded_image = image_utils.load_image_from_path_fragments(image_name, path_to_images)
    # expected is a 3 dimensional RGB NumPy Array (W,H,C)
    # test if third part of shape has 3 Channels (RGB)
    if loaded_image.shape[2] != 3:
        raise AssertionError("Expected loaded_image to have 3 dimensions, but got", loaded_image)


def test_load_image_from_full_path(image_name, path_to_images):
    full_path = image_utils.construct_image_path(image_name, path_to_images)
    loaded_image = image_utils.load_image_from_full_path(full_path)
    # expected is a 3 dimensional RGB NumPy Array (W,H,C)
    # test if third part of shape has 3 Channels (RGB)
    if loaded_image.shape[2] != 3:
        raise AssertionError("Expected loaded_image to have 3 dimensions, but got", loaded_image)


# TODO: paths correct despite first c (one lowercase, one uppercase). decide on Test-Fix in utils-issue
# until then, correct construction of path is demonstrated in other unit tests that load images
def test_construct_image_path(image_name, path_to_images):
    # expected is the correct path to the image
    image_path = image_utils.construct_image_path(image_name, path_to_images)
    expected_path = os.path.join(Path(__file__).parent.parent, "data", "TestImages", "Hand_0000002.jpg")
    if image_path != expected_path:
        raise AssertionError(f"Expected {expected_path}, but got {image_path}")
