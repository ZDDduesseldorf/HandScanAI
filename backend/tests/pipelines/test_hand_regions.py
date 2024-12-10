from pipelines.regions_utils import reorder_dict_values_from_region_dict


def test_reorder_region_dict():
    input_dict = {
        "input1": {
            "key2": "path_to_key2",
            "key3": "path_to_key3",
            "key1": "path_to_key1",
        },
        "input2": {
            "key2": "path_to_key2",
            "key1": "path_to_key1",
            "key3": "path_to_key3",
        },
    }
    right_order = ["key1", "key2", "key3"]
    test_dict_of_lists = reorder_dict_values_from_region_dict(input_dict, right_order)
    assert len(test_dict_of_lists) == 2
    assert len(test_dict_of_lists["input1"]) == 3
    assert test_dict_of_lists["input1"] == ["path_to_key1", "path_to_key2", "path_to_key3"]
