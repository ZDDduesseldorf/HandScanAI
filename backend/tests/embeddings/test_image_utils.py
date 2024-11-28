import pytest
import torch

from backend.embeddings import image_utils


### TESTS #############################################################


def test_load_image(image_name, path_to_images):
    loaded_image = image_utils.load_image(image_name, path_to_images)
    # expected is a 3 dimensional RGB Tensors (3, H, W)
    assert len(loaded_image) == 3
    assert type(loaded_image) is torch.Tensor


def test_construct_image_path(image_name, path_to_images):
    # expected is the correct path to the image
    assert (
        image_utils.construct_image_path(image_name, path_to_images) == "backend/tests/data/TestImages/Hand_0000002.jpg"
    )
