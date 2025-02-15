from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from pipelines.data_utils import build_info_knn
from pipelines.datasets import ImagePathDataset
from pipelines.distance_calculation import calculate_distance
from pipelines.inference_pipeline import _path_manager
from classifier.weighted_classification import weighted_classifier
from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import HandRegions
from utils.csv_utils import check_file_exists, check_or_create_folder, create_csv_with_header, add_entry_to_csv
from utils.key_enums import PipelineAPIKeys as APIKeys


def setup_scenario_classifier(path_to_classifier_csv, path_to_csv_age, path_to_csv_gender, header_csv):
    check_or_create_folder(path_to_classifier_csv)

    if not check_file_exists(path_to_csv_age):
        create_csv_with_header(path_to_csv_age, header_csv)

    if not check_file_exists(path_to_csv_gender):
        create_csv_with_header(path_to_csv_gender, header_csv)


def scenario_classifier(path_to_result_csv, testing=False):
    path_to_classifier_csv = path_to_result_csv / "classifier"
    path_to_csv_age = path_to_classifier_csv / "classification_data_age.csv"
    path_to_csv_gender = path_to_classifier_csv / "classification_data_gender.csv"

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

    setup_scenario_classifier(path_to_classifier_csv, path_to_csv_age, path_to_csv_gender, header_csv)

    _, _, _, _, folder_path_base = _path_manager(testing)
    dataset_base = ImagePathDataset(folder_path_base)

    for path_dict in dataset_base:
        uuid = path_dict[Keys.UUID.value]
        path = path_dict[Keys.IMAGE_PATH.value]
        k = 6
        run_generate_classifier_result(uuid, path, k, path_to_csv_age, path_to_csv_gender, testing)


def run_generate_classifier_result(uuid, image_path, k, path_to_csv_age, path_to_csv_gender, testing=False):
    """
    pipeline to classify age and gender based on the hand image

    Args:
        uuid (str): Unique identifier for the image

    Returns:
        ensemble_df: pandasdataframe(classified_age(float),min_age(float),max_age(float), confidence_age(float),
        classified_gender(0,1), confidence_gender(float))
        0:female, 1:male
    """
    _, _, embedding_csv_path, metadata_csv_path, _ = _path_manager(testing)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_normalization
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    ######## STEP 3: search nearest neighbours ###########################

    dict_all_dist = calculate_distance(dict_embedding, k, embedding_csv_path)

    dict_all_info_knn = build_info_knn(metadata_csv_path, dict_all_dist)

    dict_info_knn, age, gender = delete_same_uuid_from_nearest_neighbours(uuid, dict_all_info_knn)

    ######## STEP 4: make a decision for prediction ######################

    ensemble_df, age_dict, gender_dict = weighted_classifier(dict_info_knn)

    dict_age = {
        Keys.UUID.value: uuid,
        HandRegions.HAND_0.value: age_dict[HandRegions.HAND_0.value][APIKeys.CLASSIFIED_AGE.value].iloc[0],
        HandRegions.HANDBODY_1.value: age_dict[HandRegions.HANDBODY_1.value][APIKeys.CLASSIFIED_AGE.value].iloc[0],
        HandRegions.THUMB_2.value: age_dict[HandRegions.THUMB_2.value][APIKeys.CLASSIFIED_AGE.value].iloc[0],
        HandRegions.INDEXFINGER_3.value: age_dict[HandRegions.INDEXFINGER_3.value][APIKeys.CLASSIFIED_AGE.value].iloc[
            0
        ],
        HandRegions.MIDDLEFINGER_4.value: age_dict[HandRegions.MIDDLEFINGER_4.value][APIKeys.CLASSIFIED_AGE.value].iloc[
            0
        ],
        HandRegions.RINGFINGER_5.value: age_dict[HandRegions.RINGFINGER_5.value][APIKeys.CLASSIFIED_AGE.value].iloc[0],
        HandRegions.LITTLEFINGER_6.value: age_dict[HandRegions.LITTLEFINGER_6.value][APIKeys.CLASSIFIED_AGE.value].iloc[
            0
        ],
        "label": age,
    }

    add_entry_to_csv(path_to_csv_age, dict_age)

    dict_gender = {
        Keys.UUID.value: uuid,
        HandRegions.HAND_0.value: gender_dict[HandRegions.HAND_0.value][APIKeys.CLASSIFIED_GENDER.value].iloc[0],
        HandRegions.HANDBODY_1.value: gender_dict[HandRegions.HANDBODY_1.value][APIKeys.CLASSIFIED_GENDER.value].iloc[
            0
        ],
        HandRegions.THUMB_2.value: gender_dict[HandRegions.THUMB_2.value][APIKeys.CLASSIFIED_GENDER.value].iloc[0],
        HandRegions.INDEXFINGER_3.value: gender_dict[HandRegions.INDEXFINGER_3.value][
            APIKeys.CLASSIFIED_GENDER.value
        ].iloc[0],
        HandRegions.MIDDLEFINGER_4.value: gender_dict[HandRegions.MIDDLEFINGER_4.value][
            APIKeys.CLASSIFIED_GENDER.value
        ].iloc[0],
        HandRegions.RINGFINGER_5.value: gender_dict[HandRegions.RINGFINGER_5.value][
            APIKeys.CLASSIFIED_GENDER.value
        ].iloc[0],
        HandRegions.LITTLEFINGER_6.value: gender_dict[HandRegions.LITTLEFINGER_6.value][
            APIKeys.CLASSIFIED_GENDER.value
        ].iloc[0],
        "label": gender,
    }

    add_entry_to_csv(path_to_csv_gender, dict_gender)

    return ensemble_df


def delete_same_uuid_from_nearest_neighbours(uuid, dict_all_info_knn):
    print(uuid)
    row = dict_all_info_knn[HandRegions.HAND_0.value].loc[
        dict_all_info_knn[HandRegions.HAND_0.value][Keys.UUID.value] == uuid
    ]

    age = row[Keys.AGE.value].iloc[0]
    gender = row[Keys.GENDER.value].iloc[0]
    for _, region_df in dict_all_info_knn.items():
        region_df.reset_index(inplace=True)
        print(f"vorher : {region_df}")
        region_df.drop(region_df.loc[region_df[Keys.UUID.value] == uuid].index, inplace=True)
        print(f"nachher: {region_df}")
    return dict_all_info_knn, age, gender
