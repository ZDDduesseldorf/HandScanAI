import pytest
from pathlib import Path


@pytest.fixture()
def image_name():
    yield "Hand_0000002.jpg"


@pytest.fixture()
def path_to_base_images():
    base_dir = Path(__file__).resolve().parent.parent
    test_image_path = base_dir / "data" / "TestBaseDataset"
    yield str(test_image_path)


@pytest.fixture()
def path_to_region_images():
    base_dir = Path(__file__).resolve().parent.parent
    test_image_path = base_dir / "data" / "TestRegionDataset"
    yield str(test_image_path)
