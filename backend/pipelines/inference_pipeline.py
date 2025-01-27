from pathlib import Path

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from .data_utils import build_info_knn
from .distance_calculation import calculate_distance
from classifier.simple_classification import classify_age, classify_gender, ensemble_classifier
from classifier.weighted_classification import weighted_classify_age, weighted_classify_gender
from utils.logging_utils import logging_nearest_neighbours, logging_classification
# this file is used to generate the prediction of an image


# is triggered by the ‘Analyse Starten’ button in the frontend. Transfer of the uuid of the current image
# TODO: Wo werden Bilder aus Frontend gespeichert? -> QueryImages
def _path_manager(testing):
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
def run_inference_pipeline(uuid, testing=False):
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

    k = 5  # anzahl nächster Nachbarn
    dict_all_dist = calculate_distance(dict_embedding, k, embedding_csv_path)

    dict_all_info_knn = build_info_knn(metadata_csv_path, dict_all_dist)
    ######## STEP 4: make a decision for prediction ######################

    age_dict = classify_age(dict_all_info_knn)
    # age_dict = weighted_classify_age(dict_all_info_knn)

    gender_dict = classify_gender(dict_all_info_knn)
    # gender_dict = weighted_classify_gender(dict_all_info_knn)

    ensemble_df = ensemble_classifier(age_dict, gender_dict)

    #### Logging ####
    if not testing:
        logging_nearest_neighbours(uuid, dict_all_info_knn)
        logging_classification(uuid, age_dict, gender_dict, ensemble_df)
    return ensemble_df


# TODO: Verschieben in image_utils Datei
def get_image_path(folder_path_query, uuid):
    # TODO: correct path to image_folder
    """
    Finds and returns the file path to an image based on its UUID and supported extensions.

    Args:
        temp_base_dir (Path): The base directory. Typically derived from the current file's location.
        uuid (str): Unique identifier for the image

    Returns:
        Path: The absolute path to the image file if found.
        None: If no file with the given UUID and extensions exists in the specified folder.
    """
    extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    for ext in extensions:
        image_path = folder_path_query / f"{uuid}{ext}"
        if image_path.exists():
            return image_path.resolve()
    return None
