from enum import Enum
from logging import getLogger

logger = getLogger(__name__)


class PipelineDataframeKeys(Enum):
    """
    Used as keys for dataframe, which is output to frontend.
    """

    CLASSIFIED_AGE = "classified_age"
    MIN_AGE = "min_age"
    MAX_AGE = "max_age"
    CONFIDENCE_AGE = "confidence_age"
    CLASSIFIED_GENDER = "classified_gender"
    CONFIDENCE_GENDER = "confidence_gender"
    UUID = "uuid"
    IMAGE_PATH = "image_path"
    METADATA_GENDER = "gender"
    METADATA_AGE = "age"


class PipelineDictKeys(Enum):
    """
    Used as keys to dicts that pass data down the pipelines.
    """

    UUID = "uuid"
    EMBEDDINGS = "embeddings"
    IMAGE_PATH = "image_path"
    IMAGE_PATHS_INITIAL = "image_paths"
    IMAGE_TENSORS = "image_tensors"


class HandRegions(Enum):
    """
    Used as region keys to
    - save and load data
    - in dicts that pass data down the pipelines.
    """

    HAND_0 = "Hand"
    HANDBODY_1 = "HandBody"
    THUMB_2 = "Thumb"
    INDEXFINGER_3 = "IndexFinger"
    MIDDLEFINGER_4 = "MiddleFinger"
    RINGFINGER_5 = "RingFinger"
    LITTLEFINGER_6 = "LittleFinger"


# TODO: potentially not used anymore (hand_region_order and function). If so, delete and rename file to dict_utils o.ä.
hand_region_order = [
    HandRegions.HAND_0.value,
    HandRegions.HANDBODY_1.value,
    HandRegions.THUMB_2.value,
    HandRegions.INDEXFINGER_3.value,
    HandRegions.MIDDLEFINGER_4.value,
    HandRegions.RINGFINGER_5.value,
    HandRegions.LITTLEFINGER_6.value,
]


def reorder_dict_values_from_region_dict(
    input_dict: dict[str, dict[str, str]], right_order: list[str] = hand_region_order
):
    """
    Reorders the string values in inner dictionaries according to the given right_order.

    Args:
        input_dict (dict[str, dict[str, str]]): A dictionary with integer keys and inner dictionaries as values.
        right_order (list[str]): A list of keys specifying the desired order for the inner dictionaries.

    Returns:
        output_dict (dict[int, list[str]]): A dictionary with the same keys and ordered string lists as values.
    """
    output_dict: dict[str, list[str]] = {}

    for outer_key, inner_dict in input_dict.items():
        # Create a list of values based on right_order
        ordered_values = []
        for key in right_order:
            if key in inner_dict:
                ordered_values.append(inner_dict[key])
            else:
                logger.error(f"{key} not found for UUID {outer_key}, added -1")
                ordered_values.append(-1)
        output_dict[outer_key] = ordered_values

    return output_dict
