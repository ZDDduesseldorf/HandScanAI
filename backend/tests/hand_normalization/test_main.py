import hand_normalization.src.main as normalization
from pipelines.regions_utils import PipelineDictKeys as Keys


def test_normalize_hand_image(absolute_image_path):
    temp_uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    regions_dict = normalization.normalize_hand_image(absolute_image_path)
    # expect 7 items in image_tensors
    assert len(regions_dict) == 7
