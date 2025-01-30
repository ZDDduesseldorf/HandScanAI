from pathlib import Path

from utils.regions_utils import PipelineDictKeys as Keys
from utils.regions_utils import PipelineAPIKeys as APIKeys
from utils.csv_utils import create_csv_with_header, add_entry_to_csv
# logger für uuid, datum, uhrzeit
# rest csvs


def logging_manager():
    temp_base_dir = Path(__file__).resolve().parent.parent
    path_to_logs = temp_base_dir / "logs"

    path_to_nearest_neighbours = path_to_logs / "nearest_neighbours.csv"
    path_to_classification = path_to_logs / "classification.csv"
    path_to_input_data = path_to_logs / "input_data.csv"

    return path_to_nearest_neighbours, path_to_classification, path_to_input_data


def setup_csv_logging():
    path_to_nearest_neighbours, path_to_classification, path_to_input_data = logging_manager()

    header_nearest_neigbour = [
        Keys.UUID.value,
        Keys.REGION.value,
        Keys.NEIGHBOUR_UUID.value,
        Keys.DISTANCE.value,
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

    create_csv_with_header(path_to_nearest_neighbours, header_nearest_neigbour)
    create_csv_with_header(path_to_classification, header_classification)
    create_csv_with_header(path_to_input_data, header_input_data)


def logging_nearest_neighbours(uuid, dict_all_info_knn: dict):
    path_to_nearest_neighbours, _, _ = logging_manager()
    save_nearest_neighbours_info(uuid, dict_all_info_knn, path_to_nearest_neighbours)


def save_nearest_neighbours_info(uuid, dict_all_info_knn: dict, path_to_nearest_neighbours):
    for regionkey, regiondf in dict_all_info_knn.items():
        for _, row in regiondf.iterrows():
            dict_row = {
                Keys.UUID.value: uuid,
                Keys.REGION.value: regionkey,
                Keys.NEIGHBOUR_UUID.value: row[Keys.UUID.value],
                Keys.DISTANCE.value: row[Keys.DISTANCE.value],
                Keys.AGE.value: row[Keys.AGE.value],
                Keys.GENDER.value: row[Keys.GENDER.value],
            }
            add_entry_to_csv(path_to_nearest_neighbours, dict_row)


def logging_classification(uuid, age_dict, gender_dict, ensemble_df):
    _, path_to_classification, _ = logging_manager()
    save_classifiaction_info(uuid, age_dict, gender_dict, ensemble_df, path_to_classification)


def save_classifiaction_info(uuid, age_dict, gender_dict, ensemble_df, path_to_classification):
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


def logging_input_data(uuid, ground_truth_data: dict):
    _, _, path_to_input_data = logging_manager()
    save_input_data_info(uuid, ground_truth_data, path_to_input_data)


def save_input_data_info(uuid, ground_truth_data: dict, path_to_input_data):
    add_entry_to_csv(
        path_to_input_data,
        {
            APIKeys.UUID.value: uuid,
            APIKeys.REAL_AGE.value: ground_truth_data[APIKeys.REAL_AGE.value],
            APIKeys.REAL_GENDER.value: ground_truth_data[APIKeys.REAL_GENDER.value],
        },
    )
