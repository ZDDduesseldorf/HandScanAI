import pytest
from pathlib import Path

@pytest.fixture()
def image_name():
    yield "Hand_0000002.jpg"

@pytest.fixture()
def path_to_images():
    base_dir = Path(__file__).resolve().parent.parent
    test_image_path = base_dir / "data" / "TestImages"
    yield str(test_image_path)