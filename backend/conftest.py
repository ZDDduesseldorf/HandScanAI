import pytest

from embeddings import embeddings_utils, image_utils, models_utils


@pytest.fixture()
def image_name():
    yield "Hand_0000002.jpg"


@pytest.fixture()
def path_to_images():
    yield "backend/tests/data/TestImages/"
