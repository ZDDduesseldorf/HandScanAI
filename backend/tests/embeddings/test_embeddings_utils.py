import pytest

from embeddings import embeddings_utils
from embeddings import image_utils
from embeddings import models_utils

### FIXTURES ######################################################


@pytest.fixture()
def loaded_test_image(image_name, path_to_images):
    yield image_utils.load_image_from_path_fragments(image_name, path_to_images)


@pytest.fixture()
def loaded_test_image_array(loaded_test_image):
    loaded_image_array = [
        loaded_test_image,
        loaded_test_image,
        loaded_test_image,
        loaded_test_image,
    ]
    yield loaded_image_array


@pytest.fixture()
def test_image_name_array(image_name):
    yield [image_name, image_name]


@pytest.fixture()
def test_densenet():
    yield models_utils.load_model(models_utils.CNNModel.DENSENET_121)


@pytest.fixture()
def test_resnet():
    yield models_utils.load_model(models_utils.CNNModel.RESNET_50)


### TESTS #############################################################


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


def test_calculate_single_resnet_embedding(loaded_test_image, test_resnet):
    test_embeddings = embeddings_utils.calculate_embedding(loaded_test_image, test_resnet)
    # expected dimensions of resnet embedding are [1, 1000]
    assert test_embeddings.shape[0] == 1
    assert test_embeddings.shape[1] == 1000


def test_calculate_embeddings(loaded_test_image_array, test_densenet):
    test_embeddings = embeddings_utils.calculate_embeddings(loaded_test_image_array, test_densenet)
    # expected dimensions of densenet embedding are [1, 1024]
    assert test_embeddings[0].shape[1] == 1024
    # expected length of the resulting array is the same as input array
    assert len(test_embeddings) == len(loaded_test_image_array)


def test_calculate_embeddings_from_path(test_image_name_array, path_to_images, test_densenet):
    test_embeddings = embeddings_utils.calculate_embeddings_from_path_fragments(
        test_image_name_array, path_to_images, test_densenet
    )
    # expected dimensions of densenet embedding are [1, 1024]
    assert test_embeddings[0].shape[1] == 1024
    # expected length of the resulting array is the same as input array
    assert len(test_embeddings) == len(test_image_name_array)
