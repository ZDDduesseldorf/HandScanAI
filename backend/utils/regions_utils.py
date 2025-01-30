from enum import Enum


class PipelineAPIKeys(Enum):
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
    METADATA_GENDER = "meta_gender"
    METADATA_AGE = "meta_age"
    REAL_AGE = "real_age"
    REAL_GENDER = "real_gender"


class PipelineDictKeys(Enum):
    """
    Used as keys to dicts that pass data down the pipelines.
    """

    UUID = "uuid"
    EMBEDDINGS = "embeddings"
    IMAGE_PATH = "image_path"
    IMAGE_PATHS_INITIAL = "image_paths"
    IMAGE_TENSORS = "image_tensors"
    SAVED_EMBEDDINGS = "saved_embeddings"
    DISTANCE = "distance"
    DISTANCE_IDS_SORTED = "distance_ids_sorted"
    AGE = "age"
    GENDER = "gender"
    REGION = "region"
    NEIGHBOUR_UUID = "neighbour_uuid"


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
