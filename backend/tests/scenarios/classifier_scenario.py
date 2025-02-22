from pathlib import Path
import pandas as pd
from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from pipelines.data_utils import build_info_knn_from_csv
from pipelines.datasets import ImagePathDataset
from pipelines.distance_calculation import calculate_cosine_distance
from pipelines.inference_pipeline import _path_manager
from classifier.weighted_classification import weighted_classifier
from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import HandRegions
from utils.csv_utils import check_file_exists, check_or_create_folder, create_csv_with_header, add_entry_to_csv
from utils.key_enums import PipelineAPIKeys as APIKeys
from utils.logging_utils import save_classification_info
# TODO: comment in to run the classifier_scenario
# from tests.scenarios.embeddings_scenario import scenario_path_manager

"""
Prerequisites:
To run this scenario, the base dataset of the application needs to be set up and filled correctly (BaseImages, RegionImages and the corresponding Embeddings.csvs, Metadata.csv).
For more information on how to do that, see Readme of the pipelines-module or setup_new_project_data in manage.py.

To run this scenario, comment in the function test_scenario_classifier below.
Then run it on the console from the /backend-folder via 'pytest -s tests/scenarios/classifier_scenario.py'.

Comment it out again afterwards to not run it as unit test in ci-pipeline.
"""

# TODO: comment in to run the classifier_scenario
"""def test_scenario_classifier():
    path_to_result_csv_folder = scenario_path_manager()
    scenario_classifier(path_to_result_csv_folder, testing=False)"""


def scenario_classifier(path_to_result_csv_folder: Path, testing: bool = False):
    """
    This function classifies every image in BaseImages and saves the results for evaluation.
    Saved results are those of the region classifiers as well as the ensemble classifiers for age and gender.

    It specifies the necessary paths and headers for the csvs and sets up the scenario file structure.

    It also specifies the k that is used in the test run (k = number of nearest neighbours used for the classification).

    Note that after each run, the result csvs need to be moved or renamed to not mix up classification results with those of previous runs.
    The correctly named files serve as the input data for the random_forest-scenario (see random_forest_feature_importance_scenario.py for further information.)

    Args:
        path_to_result_csv (Path): absolute path to default folder to save scenario-csvs
        testing (bool, optional): flag whether or not to use the path to the Test-BaseImages or the prod-BaseImages.
            Defaults to False since we want to use prod-data for the scenarios. Testing-data can be used to testrun new implementations.
    """
    path_to_classifier_folder = path_to_result_csv_folder / "classifier"
    path_to_csv_age = path_to_classifier_folder / "classification_data_age.csv"
    path_to_csv_gender = path_to_classifier_folder / "classification_data_gender.csv"
    path_to_csv_ensemble = path_to_classifier_folder / "classification_data_ensemble.csv"

    header_csv = [
        Keys.UUID.value,
        HandRegions.HAND_0.value,
        HandRegions.HANDBODY_1.value,
        HandRegions.THUMB_2.value,
        HandRegions.INDEXFINGER_3.value,
        HandRegions.MIDDLEFINGER_4.value,
        HandRegions.RINGFINGER_5.value,
        HandRegions.LITTLEFINGER_6.value,
        "label",
    ]

    header_ensemble = [
        APIKeys.UUID.value,
        Keys.REGION.value,
        APIKeys.CLASSIFIED_AGE.value,
        APIKeys.MIN_AGE.value,
        APIKeys.MAX_AGE.value,
        APIKeys.CONFIDENCE_AGE.value,
        APIKeys.CLASSIFIED_GENDER.value,
        APIKeys.CONFIDENCE_GENDER.value,
    ]

    setup_scenario_classifier(
        path_to_classifier_folder,
        path_to_csv_age,
        path_to_csv_gender,
        header_csv,
        path_to_csv_ensemble,
        header_ensemble,
    )

    _, _, _, _, folder_path_base = _path_manager(testing)
    dataset_base = ImagePathDataset(folder_path_base)

    for path_dict in dataset_base:
        uuid = path_dict[Keys.UUID.value]
        image_path = path_dict[Keys.IMAGE_PATH.value]
        ### SPECIFY k
        k = 5
        run_generate_classifier_result(
            uuid, image_path, k, path_to_csv_age, path_to_csv_gender, path_to_csv_ensemble, testing
        )


def setup_scenario_classifier(
    path_to_classifier_folder: Path,
    path_to_csv_age: Path,
    path_to_csv_gender: Path,
    header_csv: list[str],
    path_to_csv_ensemble: Path,
    header_ensemble: list[str],
):
    """
    This function checks if the necessary folders and files for the classification scenario already exist and if they don't, creates them.

    Args:
        path_to_classifier_folder (Path): absolute path to /result_csvs/classifier
        path_to_csv_age (Path): absolute path to csv that contains region classification results for age
        path_to_csv_gender (Path): absolute path to csv that contains region classification results for gender
        header_csv (list[str]): list describing the header of the csvs for region classification results
        path_to_csv_ensemble (Path): absolute path to csv that contains ensemble classification results for both age and gender
        header_ensemble (list[str]): list describing the header of the csv for ensemble classification results
    """
    check_or_create_folder(path_to_classifier_folder)

    if not check_file_exists(path_to_csv_age):
        create_csv_with_header(path_to_csv_age, header_csv)

    if not check_file_exists(path_to_csv_gender):
        create_csv_with_header(path_to_csv_gender, header_csv)

    if not check_file_exists(path_to_csv_ensemble):
        create_csv_with_header(path_to_csv_ensemble, header_ensemble)


def run_generate_classifier_result(
    uuid: str,
    image_path: Path,
    k: int,
    path_to_csv_age: Path,
    path_to_csv_gender: Path,
    path_to_csv_ensemble: Path,
    testing: bool = False,
) -> pd.DataFrame:
    """
    Pipeline to classify age and gender based on the hand image and save the region as well as ensemble results in csv files.

    Args:
        uuid (str): Unique identifier for the image
        image_path (Path): absolute path to query image (image to be classified)
        k (int): number of nearest neighbours used for classification
        path_to_csv_age (Path): absolute path to csv that contains region classification results for age
        path_to_csv_gender (Path): absolute path to csv that contains region classification results for gender
        path_to_csv_ensemble (Path): absolute path to csv that contains ensemble classification results for both age and gender
        testing (bool, optional): flag whether or not to use the path-manager's paths test or prod paths. Defaults to False since we want to use prod data for the test scenarios.

    Returns:
        ensemble_df (pd.DataFrame): contains the columns
        - classified_age(float)
        - min_age(float)
        - max_age(float)
        - confidence_age(float)
        - classified_gender(0,1) with values 0:female, 1:male
        - confidence_gender(float)
    """
    _, _, embedding_csv_path, metadata_csv_path, _ = _path_manager(testing)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_normalization
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    ######## STEP 3: search nearest neighbours ###########################

    dict_all_dist = calculate_cosine_distance(dict_embedding, k, embedding_csv_path)

    dict_all_info_knn = build_info_knn_from_csv(metadata_csv_path, dict_all_dist)

    dict_info_knn, age, gender = delete_same_uuid_from_nearest_neighbours(uuid, dict_all_info_knn)

    ######## STEP 4: make a decision for prediction ######################

    # TODO: for simple (unweighted) classification use simple_classifier
    ensemble_df, age_dict, gender_dict = weighted_classifier(dict_info_knn)

    save_classification_info(uuid, age_dict, gender_dict, ensemble_df, path_to_csv_ensemble, add_region_logging=False)
    # age
    save_region_results_for_key(
        uuid=uuid,
        classification_dict=age_dict,
        dict_key=APIKeys.CLASSIFIED_AGE.value,
        label=age,
        path_to_csv_file=path_to_csv_age,
    )
    # gender
    save_region_results_for_key(
        uuid=uuid,
        classification_dict=gender_dict,
        dict_key=APIKeys.CLASSIFIED_GENDER.value,
        label=gender,
        path_to_csv_file=path_to_csv_gender,
    )

    return ensemble_df


def save_region_results_for_key(
    uuid: str, classification_dict: dict, dict_key: str, label: (int | float), path_to_csv_file: Path
):
    """
    Generic method to read the classification data from either age or gender into a new dict and save it with the corresponding true label in the respective csv-file.

    Args:
        uuid (str): unique identifier of an image
        classification_dict (dict): holds the results of the region-classifications
        dict_key (str): key with which the result of the respective region classification can be read from the dict (either for gender or age)
        label (int  |  float): the correct label-value for the datapoint (correct gender or correct age)
        path_to_csv_file (Path): absolute path to the respective csv to save the classification data in (either to csv_gender or csv_age)

    Examples:
        ```
        # age
        save_region_results_for_key(
            uuid=uuid,
            classification_dict=age_dict,
            dict_key=APIKeys.CLASSIFIED_AGE.value,
            label=age,
            path_to_csv_file=path_to_csv_age,
        )
        # gender
        save_region_results_for_key(
            uuid=uuid,
            classification_dict=gender_dict,
            dict_key=APIKeys.CLASSIFIED_GENDER.value,
            label=gender,
            path_to_csv_file=path_to_csv_gender,
        )
        ```
    """
    dict_classification_entry = {
        Keys.UUID.value: uuid,
        HandRegions.HAND_0.value: classification_dict[HandRegions.HAND_0.value][dict_key].iloc[0],
        HandRegions.HANDBODY_1.value: classification_dict[HandRegions.HANDBODY_1.value][dict_key].iloc[0],
        HandRegions.THUMB_2.value: classification_dict[HandRegions.THUMB_2.value][dict_key].iloc[0],
        HandRegions.INDEXFINGER_3.value: classification_dict[HandRegions.INDEXFINGER_3.value][dict_key].iloc[0],
        HandRegions.MIDDLEFINGER_4.value: classification_dict[HandRegions.MIDDLEFINGER_4.value][dict_key].iloc[0],
        HandRegions.RINGFINGER_5.value: classification_dict[HandRegions.RINGFINGER_5.value][dict_key].iloc[0],
        HandRegions.LITTLEFINGER_6.value: classification_dict[HandRegions.LITTLEFINGER_6.value][dict_key].iloc[0],
        "label": label,
    }

    add_entry_to_csv(path_to_csv_file, dict_classification_entry)


def delete_same_uuid_from_nearest_neighbours(uuid: str, dict_all_info_knn: dict) -> tuple[dict, int, int]:
    """
    This function deletes the uuid of the query image from the dict with the nearest neighbour infos and returns the corresponding age and gender from its metadata.

    Deleting the datapoint from the dict is necessary because the classifier scenario runs query images that are part of the base dataset.
    To not classify a query image with its own copy, it gets removed from the dict_all_info_knn that holds the information about the nearest neighbours.
    This would not be a concern in regular inference because query images get saved into the base dataset only after they were classified.

    The correct age and gender of the datapoint are extracted and returned as well for convenience, since they will be needed further down the pipeline.

    Args:
        uuid (str): unique identifier of an image
        dict_all_info_knn (dict): dictionary that contains the necessary information about the nearest neighbours of an image used to classify it.

    Returns:
        (dict_all_info_knn, age, gender) (dict, int, int):
        - dict_all_info_knn: the nearest neighbour data for the given uuid cleared of its own data
        - age: the correct age corresponding to the uuid
        - gender: the correct gender corresponding to the uuid
    """
    print(uuid)
    row = dict_all_info_knn[HandRegions.HAND_0.value].loc[
        dict_all_info_knn[HandRegions.HAND_0.value][Keys.UUID.value] == uuid
    ]

    age = row[Keys.AGE.value].iloc[0]
    gender = row[Keys.GENDER.value].iloc[0]
    for _, region_df in dict_all_info_knn.items():
        region_df.reset_index(inplace=True)
        region_df.drop(region_df.loc[region_df[Keys.UUID.value] == uuid].index, inplace=True)
    return dict_all_info_knn, age, gender
