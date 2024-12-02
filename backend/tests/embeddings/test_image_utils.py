import torch
import os
from backend.embeddings import image_utils
from pathlib import Path


### TESTS #############################################################


def test_load_image(image_name, path_to_images):
    loaded_image = image_utils.load_image(image_name, path_to_images)
    # expected is a 3 dimensional RGB Tensors (3, H, W)
    if len(loaded_image) != 3:
        raise AssertionError("Expected loaded_image to have 3 dimensions, but got {len(loaded_image)}")
    if not isinstance(loaded_image, torch.Tensor):
        raise AssertionError("Expected loaded_image to be a torch.Tensor")


def test_construct_image_path(image_name, path_to_images):
    # expected is the correct path to the image
    image_path = image_utils.construct_image_path(image_name, path_to_images)
    expected_path = os.path.join(Path(__file__).parent.parent, "data", "TestImages", "Hand_0000002.jpg")
    if image_path != expected_path:
        raise AssertionError(f"Expected {expected_path}, but got {image_path}")
