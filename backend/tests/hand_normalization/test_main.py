import hand_normalization.src.main as normalization


def test_normalize_hand_image(absolute_image_path):
    regions_dict = normalization.normalize_hand_image(absolute_image_path)
    # expect 7 items in image_tensors
    assert len(regions_dict) == 7
