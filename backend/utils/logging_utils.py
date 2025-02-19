from pathlib import Path
from datetime import datetime
import pandas as pd

from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import PipelineAPIKeys as APIKeys
from utils.csv_utils import create_csv_with_header, add_entry_to_csv, check_or_create_folder, check_file_exists

# This module contains functions for logging. The logging used in the pipelines uses default paths. The respective functions start with "logging_" and contain notes in the docstrings.
# The functions not containing the default path are needed in test scenarios to not overwrite the production-logs.


def logging_manager() -> tuple[Path, Path, Path, Path]:
    """
    Provides the paths to the logs-folder and the log-csv-files.
    Folder-path contains current date to structure logfiles by date.

    Returns:
        paths (tuple[Path, Path, Path, Path]): contains in this order:
        path_to_logs (str) (logs-folder),
        path_to_nearest_neighbour (str) (csv-file),
        path_to_classification (str) (csv-file),
        path_to_input_data (str) (csv-file)

    Example:
    use like `path_to_logs, path_to_nearest_neighbours, path_to_classification, path_to_input_data = logging_manager()`

    """
    temp_base_dir = Path(__file__).resolve().parent.parent

    date = datetime.now()
    formatted_date = date.strftime("%Y-%m-%d")

    path_to_logs = temp_base_dir / "logs" / formatted_date
    path_to_nearest_neighbours = path_to_logs / "nearest_neighbours.csv"
    path_to_classification = path_to_logs / "classification.csv"
    path_to_input_data = path_to_logs / "input_data.csv"

    return path_to_logs, path_to_nearest_neighbours, path_to_classification, path_to_input_data


def setup_csv_logging():
    """
    Creates the logs-folder and the log-csv-files with the correct headers.
    """
    path_to_logs, path_to_nearest_neighbours, path_to_classification, path_to_input_data = logging_manager()

    header_nearest_neigbour = [
        Keys.UUID.value,
        Keys.REGION.value,
        Keys.NEIGHBOUR_UUID.value,
        Keys.SIMILARITY.value,
        Keys.AGE.value,
        Keys.GENDER.value,
    ]

    header_classification = [
        APIKeys.UUID.value,
        Keys.REGION.value,
        APIKeys.CLASSIFIED_AGE.value,
        APIKeys.MIN_AGE.value,
        APIKeys.MAX_AGE.value,
        APIKeys.CONFIDENCE_AGE.value,
        APIKeys.CLASSIFIED_GENDER.value,
        APIKeys.CONFIDENCE_GENDER.value,
    ]

    header_input_data = [APIKeys.UUID.value, APIKeys.REAL_AGE.value, APIKeys.REAL_GENDER.value]

    check_or_create_folder(path_to_logs)

    if not check_file_exists(path_to_nearest_neighbours):
        create_csv_with_header(path_to_nearest_neighbours, header_nearest_neigbour)

    if not check_file_exists(path_to_classification):
        create_csv_with_header(path_to_classification, header_classification)

    if not check_file_exists(path_to_input_data):
        create_csv_with_header(path_to_input_data, header_input_data)


def logging_nearest_neighbours(uuid: str, dict_all_info_knn: dict):
    """
    Default logging in pipelines for production.
    Uses the default logs-path to save the information from the dict to the log-csv for nearest neighbours

    Args:
        uuid (str): identifier of the datapoint
        dict_all_info_knn (dict): dict that contains information about the nearest neighbours identified per hand-region for the datapoint
    """
    _, path_to_nearest_neighbours, _, _ = logging_manager()
    save_nearest_neighbours_info(uuid, dict_all_info_knn, path_to_nearest_neighbours)


def save_nearest_neighbours_info(uuid: str, dict_all_info_knn: dict, path_to_nearest_neighbours: (Path | str)):
    """
    Saves the information from the dict to the log-csv for nearest neighbours at the specified path.

    Args:
        uuid (str): identifier of the datapoint
        dict_all_info_knn (dict): dict that contains information about the nearest neighbours identified per hand-region for the datapoint
        path_to_nearest_neighbours (Path | str): absolute path to the log-csv-file for nearest neoghbours
    """
    for regionkey, regiondf in dict_all_info_knn.items():
        for _, row in regiondf.iterrows():
            dict_row = {
                Keys.UUID.value: uuid,
                Keys.REGION.value: regionkey,
                Keys.NEIGHBOUR_UUID.value: row[Keys.UUID.value],
                Keys.SIMILARITY.value: row[Keys.SIMILARITY.value],
                Keys.AGE.value: row[Keys.AGE.value],
                Keys.GENDER.value: row[Keys.GENDER.value],
            }
            add_entry_to_csv(path_to_nearest_neighbours, dict_row)


def logging_classification(uuid: str, age_dict: dict, gender_dict: dict, ensemble_df: pd.DataFrame):
    """
    Default logging in pipelines for production.
    Uses the default logs-path to save information about the classification steps per region and ensemble to the log-csv for classification.

    Args:
        uuid (str): identifier of the datapoint
        age_dict (dict): contains the information for the age classifications per region for the datapoint
        gender_dict (dict): contains the information for the gender classifications per region for the datapoint
        ensemble_df (pd.DataFrame): contains the information for the ensemble classification per datapoint
    """
    _, _, path_to_classification, _ = logging_manager()
    save_classifiaction_info(uuid, age_dict, gender_dict, ensemble_df, path_to_classification)


def save_classifiaction_info(
    uuid: str, age_dict: dict, gender_dict: dict, ensemble_df: pd.DataFrame, path_to_classification: (Path | str)
):
    """
    Saves information about the classification steps per region and ensemble to the log-csv for classification at the specified path.

    Args:
        uuid (str): identifier of the datapoint
        age_dict (dict): contains the information for the age classifications per region for the datapoint
        gender_dict (dict): contains the information for the gender classifications per region for the datapoint
        ensemble_df (pd.DataFrame): contains the information for the ensemble classification per datapoint
        path_to_classification (Path | str): absolute path to the log-csv-file for classification
    """
    for regionkey, region_age_df in age_dict.items():
        region_gender_df = gender_dict[regionkey]
        dict_row = {
            APIKeys.UUID.value: uuid,
            Keys.REGION.value: regionkey,
            APIKeys.CLASSIFIED_AGE.value: region_age_df.loc[0, APIKeys.CLASSIFIED_AGE.value],
            APIKeys.MIN_AGE.value: "N/A",
            APIKeys.MAX_AGE.value: "N/A",
            APIKeys.CONFIDENCE_AGE.value: region_age_df.loc[0, APIKeys.CONFIDENCE_AGE.value],
            APIKeys.CLASSIFIED_GENDER.value: region_gender_df.loc[0, APIKeys.CLASSIFIED_GENDER.value],
            APIKeys.CONFIDENCE_GENDER.value: region_gender_df.loc[0, APIKeys.CONFIDENCE_GENDER.value],
        }
        add_entry_to_csv(path_to_classification, dict_row)

    dict_row = {
        APIKeys.UUID.value: uuid,
        Keys.REGION.value: "gesamt",
        APIKeys.CLASSIFIED_AGE.value: ensemble_df.loc[0, APIKeys.CLASSIFIED_AGE.value],
        APIKeys.MIN_AGE.value: ensemble_df.loc[0, APIKeys.MIN_AGE.value],
        APIKeys.MAX_AGE.value: ensemble_df.loc[0, APIKeys.MAX_AGE.value],
        APIKeys.CONFIDENCE_AGE.value: ensemble_df.loc[0, APIKeys.CONFIDENCE_AGE.value],
        APIKeys.CLASSIFIED_GENDER.value: ensemble_df.loc[0, APIKeys.CLASSIFIED_GENDER.value],
        APIKeys.CONFIDENCE_GENDER.value: ensemble_df.loc[0, APIKeys.CONFIDENCE_GENDER.value],
    }
    add_entry_to_csv(path_to_classification, dict_row)


def logging_input_data(uuid: str, ground_truth_data: dict):
    """
    Default logging in pipelines for production.
    Uses the default logs-path to save information about the correct metadata input for the datapoint to the log-csv for input data.

    Args:
        uuid (str): identifier of the datapoint
        ground_truth_data (dict): contains the uuid and the metadata correct age and gender of the datapoint
    """
    _, _, _, path_to_input_data = logging_manager()
    save_input_data_info(uuid, ground_truth_data, path_to_input_data)


def save_input_data_info(uuid: str, ground_truth_data: dict, path_to_input_data: (Path | str)):
    """
    Saves information about the correct metadata input for the datapoint to the log-csv for input data at the specified path.

    Args:
        uuid (str): identifier of the datapoint
        ground_truth_data (dict): contains the uuid and the metadata correct age and gender of the datapoint
        path_to_input_data (Path | str): absolute path to the log-csv-file for input data
    """
    add_entry_to_csv(
        path_to_input_data,
        {
            APIKeys.UUID.value: uuid,
            APIKeys.REAL_AGE.value: ground_truth_data[APIKeys.REAL_AGE.value],
            APIKeys.REAL_GENDER.value: ground_truth_data[APIKeys.REAL_GENDER.value],
        },
    )
