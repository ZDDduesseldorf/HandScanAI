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

"""
This file is used to generate the prediction of an image
Inference-Pipeline is triggered by the ‘Analyse Starten’ button in the frontend. Transfer of the uuid of the current image

Preparation:
The embeddings of the data set must be calculated and saved either as csvs or in milvus, as well as the associated metadata. For more information see initial-data-pipeline

"""


def _path_manager(testing: bool):
    """
    Specifies the paths to the folders in which the dataset data is stored. The dataset contains the base, region and query images as well as a csv folder with the files Metadata.csv and region_Embeddings.csv.
    Differentiation between test data and production data by flag

    Args:
        testing (bool): Flag for the use of test data (true) or the use of productive data (false)

    Returns:
        folder_path_query (str): folder,
        folder_path_region (str): folder,
        embedding_csv_path (str): folder,
        metadata_csv_path (str): csv-file,
        folder_path_base (str): folder
    """
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
    uuid: str,
    k: int = 10,
    testing: bool = False,
    use_milvus: bool = True,
    milvus_collection_name: str = milvus_collection_name,
    milvus_default_search_params: dict[str, any] = milvus_default_search_params,
):
    """
    Pipeline to classify age and gender based on the hand image.
    The pipeline can be carried out with both the test data and the production data, for which the corresponding paths are loaded from the pathmanger.

    Productiv:
    Hand image to be classified must be in folder QueryImages.
    First, the image is loaded from the productive data and normalised.
    Then the embeddings are calculated with the default model.
    Then the nearest neighbours can be searched using the embeddings of the base set stored in the csv or the vector database (Milvus).
    - The csv is used to calculate the cosine distance and in the next step the similarity is calculated based on the distance.
    - The cosine similarity is calculated using Milvus.
    Based on the metadata of the nearest neighbours, the age and gender are classified with an unweighted/weighted classifier (simple_classifier.py/weighted_classifier.py)
    The result of the classification and the metadata of the n nearest neighbours are stored in a data frame for the frontend.
    Also the result of the nearest neighbour search and the classification are logged in csvs.

    Test:
    Hand image to be classified must be in folder BaseImages.
    For testing the region_Embedding.csv are used to calculate the cosine.
    And the results are not logged.


    Args:
        uuid (str): Unique identifier for the image
        k (int, optional): _description_. Defaults to 10.
        testing (bool, optional): _description_. Defaults to False.
        use_milvus (bool, optional): _description_. Defaults to True.
        milvus_collection_name (str, optional): Name of the Milvus collection. Defaults to milvus_collection_name (milvus.py).
        milvus_default_search_params (dict[str, any], optional): Parameters for the search query. Defaults to milvus_default_search_params (milvus.py).

    Returns:
        ensemble_df: pd.dataframe(classified_age(float),min_age(float),max_age(float), confidence_age(float),
        classified_gender(0,1), confidence_gender(float))
        0:female, 1:male
        knn_info_df: pd.dataframe(region, uuid, age, gender) with n rows
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

    # TODO: for simple (unweighted) classification use simple_classifier
    ensemble_df, age_dict, gender_dict = weighted_classifier(dict_all_info_knn)

    knn_info_df = find_most_similar_nearest_neighbours(dict_all_info_knn)

    ### Logging ####
    # in case of errors, make sure logging has been setup correctly
    if not testing:
        logging_nearest_neighbours(uuid, dict_all_info_knn)
        logging_classification(uuid, age_dict, gender_dict, ensemble_df)
    return ensemble_df, knn_info_df
