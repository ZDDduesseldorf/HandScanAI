import pytest
import torch
import numpy as np
from pathlib import Path

from embeddings import embeddings_utils
from embeddings import models_utils
from utils.key_enums import HandRegions
from utils import image_utils
from hand_normalization.src.main import normalize_hand_image

### FIXTURES ######################################################


@pytest.fixture()
def image_name():
    yield "514f53d0-6aab-4da1-b929-8f1dc0817289.jpg"


@pytest.fixture()
def path_to_images():
    base_dir = Path(__file__).resolve().parent.parent
    test_image_path = base_dir / "data" / "TestBaseDataset"
    yield test_image_path


@pytest.fixture()
def absolute_image_path(path_to_images, image_name):
    yield str(path_to_images / image_name)


@pytest.fixture()
def loaded_test_image(image_name, path_to_images):
    yield image_utils.load_image_from_path_fragments(image_name, path_to_images)


@pytest.fixture()
def test_densenet():
    yield models_utils.load_model(models_utils.CNNModel.DENSENET_121)


@pytest.fixture()
def test_resnet():
    yield models_utils.load_model(models_utils.CNNModel.RESNET_50)


@pytest.fixture()
def region_dict():
    base_dir = Path(__file__).resolve().parent.parent
    path_to_region_images = base_dir / "data" / "TestRegionDataset"
    dict = {
        HandRegions.HAND_0.value: path_to_region_images / "614f53d0-6aab-4da1-b929-8f1dc0817289_Hand.bmp",
        HandRegions.HANDBODY_1.value: path_to_region_images / "614f53d0-6aab-4da1-b929-8f1dc0817289_HandBody.bmp",
        HandRegions.INDEXFINGER_3.value: path_to_region_images / "614f53d0-6aab-4da1-b929-8f1dc0817289_IndexFinger.bmp",
        HandRegions.LITTLEFINGER_6.value: path_to_region_images
        / "614f53d0-6aab-4da1-b929-8f1dc0817289_LittleFinger.bmp",
        HandRegions.MIDDLEFINGER_4.value: path_to_region_images
        / "614f53d0-6aab-4da1-b929-8f1dc0817289_MiddleFinger.bmp",
        HandRegions.RINGFINGER_5.value: path_to_region_images / "614f53d0-6aab-4da1-b929-8f1dc0817289_RingFinger.bmp",
        HandRegions.THUMB_2.value: path_to_region_images / "614f53d0-6aab-4da1-b929-8f1dc0817289_Thumb.bmp",
    }
    yield dict


### UNIT TESTS #############################################################


def test_preprocess_image(loaded_test_image):
    image_tensor = embeddings_utils.preprocess_image(loaded_test_image)
    # expected dimensions of preprocessed tensor are [1, 3, 224, 224]
    assert image_tensor.shape[0] == 1
    assert image_tensor.shape[1] == 3
    assert image_tensor.shape[2] == 224
    assert image_tensor.shape[3] == 224


def test_calculate_single_densenet_embedding(loaded_test_image, test_densenet):
    test_embeddings = embeddings_utils.calculate_embedding(loaded_test_image, test_densenet)
    # expected dimensions of densenet embedding are [1, 1024]
    assert test_embeddings.shape[0] == 1
    assert test_embeddings.shape[1] == 1024


def test_calculate_normalize_embedding(loaded_test_image, test_densenet):
    test_embeddings = embeddings_utils.calculate_embedding(loaded_test_image, test_densenet)
    normalized_embedding = embeddings_utils.normalize_embedding(test_embeddings)

    # expected dimensions of densenet embedding are [1, 1024]
    assert test_embeddings.shape[0] == 1
    assert test_embeddings.shape[1] == 1024
    assert len(normalized_embedding) == 1024

    # expect original embeddings to have values over 1 and under -1 and normalized embeddings to stay within the bounds
    test_embeddings_vector = test_embeddings.numpy()[0]
    assert np.any((test_embeddings_vector > 1) | (test_embeddings_vector < -1))
    assert not np.any((normalized_embedding > 1) | (normalized_embedding < -1))


def test_calculate_single_resnet_embedding(loaded_test_image, test_resnet):
    test_embeddings = embeddings_utils.calculate_embedding(loaded_test_image, test_resnet)
    # expected dimensions of resnet embedding are [1, 1000]
    assert test_embeddings.shape[0] == 1
    assert test_embeddings.shape[1] == 1000


def test_calculate_embeddings_from_path_dict(region_dict: dict):
    """
    also tests if default densenet_model works correctly
    """
    embeddings_dict: dict[str, torch.Tensor] = embeddings_utils.calculate_embeddings_from_path_dict(region_dict)
    # expect the result dict to have the same amount of keys as the input dict
    assert len(embeddings_dict) == len(region_dict)
    # expect the result dict to have the same keys as the input dict
    assert embeddings_dict.keys() == region_dict.keys()
    # expect the embedding-value to have the correct length for the densenet used per default (1024)
    assert embeddings_dict[HandRegions.HAND_0.value].shape[1] == 1024


def test_calculate_embeddings_with_resnet(region_dict: dict, test_resnet):
    test_embeddings = embeddings_utils.calculate_embeddings_from_path_dict(region_dict, test_resnet)
    # expected dimensions of resnet embedding are [1, 1000]
    assert test_embeddings[HandRegions.HAND_0.value].shape[1] == 1000
    # expected length of the resulting array is the same as input dict
    assert len(test_embeddings) == len(test_embeddings)


### INTEGRATION TESTS #############################################################


def test_calculate_embeddings_from_tensor_dict(absolute_image_path):
    # use hand_normalization
    region_numarray_dict = normalize_hand_image(absolute_image_path)
    embeddings_dict: dict[str, torch.Tensor] = embeddings_utils.calculate_embeddings_from_tensor_dict(
        region_numarray_dict
    )
    # expect the result dict to have the same amount of keys as the input dict
    assert len(embeddings_dict) == len(region_numarray_dict)
    # expect the result dict to have the same keys as the input dict
    assert embeddings_dict.keys() == region_numarray_dict.keys()
    # expect the embedding-value to have the correct length for the densenet used per default (1024)
    assert embeddings_dict[HandRegions.HAND_0.value].shape[1] == 1024
