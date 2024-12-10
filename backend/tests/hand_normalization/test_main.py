import hand_normalization.src.main as normalization
from pipelines.regions_utils import PipelineDictKeys as Keys


def test_normalize_hand_image(absolute_image_path):
    temp_uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    region_image_dict = normalization.normalize_hand_image(temp_uuid, absolute_image_path)
    # expect uuid to be in correct place in output dict
    assert region_image_dict[Keys.UUID.value] == temp_uuid
    # expect 7 items in image_tensors
    assert len(region_image_dict[Keys.IMAGE_TENSORS.value]) == 7
