from pathlib import Path

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from utils.image_utils import get_image_path
from .data_utils import (
    build_info_knn_from_milvus,
    build_info_knn_from_csv,
    find_most_similar_nearest_neighbours,
)
from .distance_calculation import calculate_cosine_distance
from classifier.weighted_classification import weighted_classifier
from utils.logging_utils import logging_nearest_neighbours, logging_classification
from vectordb.milvus import (
    search_embeddings_dict,
    milvus_collection_name,
    milvus_default_search_params,
)
# this file is used to generate the prediction of an image


# is triggered by the ‘Analyse Starten’ button in the frontend. Transfer of the uuid of the current image
def _path_manager(testing):
    # TODO: docstring
    temp_base_dir = Path(__file__).resolve().parent.parent
    if testing:
        folder_path_query = temp_base_dir / "tests" / "data" / "TestBaseDataset"
        folder_path_region = temp_base_dir / "tests" / "data" / "TestRegionDataset"
        embedding_csv_path = temp_base_dir / "tests" / "data" / "csv"
        metadata_csv_path = temp_base_dir / "tests" / "data" / "csv" / "Test_Hands_filtered_metadata.csv"
        folder_path_base = temp_base_dir / "tests" / "data" / "TestBaseDataset"

    else:
        folder_path_query = temp_base_dir / "app" / "media" / "QueryImages"
        folder_path_region = temp_base_dir / "app" / "media" / "RegionImages"
        embedding_csv_path = temp_base_dir / "app" / "media" / "csv"
        metadata_csv_path = temp_base_dir / "app" / "media" / "csv" / "Metadata.csv"
        folder_path_base = temp_base_dir / "app" / "media" / "BaseImages"

    return folder_path_query, folder_path_region, embedding_csv_path, metadata_csv_path, folder_path_base


# TODO pydoc
def run_inference_pipeline(
    uuid,
    k=5,
    testing=False,
    use_milvus=True,
    milvus_collection_name=milvus_collection_name,
    milvus_default_search_params=milvus_default_search_params,
):
    """
    pipeline to classify age and gender based on the hand image

    Args:
        uuid (str): Unique identifier for the image

    Returns:
        ensemble_df: pandasdataframe(classified_age(float),min_age(float),max_age(float), confidence_age(float),
        classified_gender(0,1), confidence_gender(float))
        0:female, 1:male
    """
    folder_path_query, _, embedding_csv_path, metadata_csv_path, _ = _path_manager(testing)

    ######## STEP 0: build path to image #################################

    image_path = get_image_path(folder_path_query, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_normalization
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    ######## STEP 3: search nearest neighbours ###########################
    if testing or not use_milvus:
        # for testing purposes/ if milvus is not available
        dict_all_dist = calculate_cosine_distance(dict_embedding, k, embedding_csv_path)

        dict_all_info_knn = build_info_knn_from_csv(metadata_csv_path, dict_all_dist)
    else:
        dict_all_similarities = search_embeddings_dict(
            dict_embedding, milvus_collection_name, milvus_default_search_params, k
        )

        dict_all_info_knn = build_info_knn_from_milvus(metadata_csv_path, dict_all_similarities)
    ######## STEP 4: make a decision for prediction ######################

    # TODO: für einfache Klassifizierung verwende simple_classifier
    ensemble_df, age_dict, gender_dict = weighted_classifier(dict_all_info_knn)

    knn_info_df = find_most_similar_nearest_neighbours(dict_all_info_knn)

    #### Logging ####
    if not testing:
        logging_nearest_neighbours(uuid, dict_all_info_knn)
        logging_classification(uuid, age_dict, gender_dict, ensemble_df)
    return ensemble_df, knn_info_df
