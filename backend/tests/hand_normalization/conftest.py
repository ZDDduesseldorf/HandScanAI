import pytest
from pathlib import Path


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
