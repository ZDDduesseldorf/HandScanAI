import numpy as np
import statistics
import pandas as pd

from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import PipelineAPIKeys as APIKeys

# TODO: Readme


def classify_age(dict_all_info_knn):
    """
    simple classifier for age prediction. Calculates the mean of the age per region

    Args:
        dict_all_info_knn: dict {regionkey(str): region_df(uuid, distance, age, gender)}

    Returns:
        dict_age: dict{regionkey(str): region_mean_df(mean_distance, mean_age)}
    """
    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_AGE.value, APIKeys.CLASSIFIED_AGE.value])
        age_list = region_df[Keys.AGE.value].to_list()
        age_mean = np.mean(age_list)

        distance_list = region_df[Keys.DISTANCE.value].to_list()
        distance_mean = np.mean(distance_list)
        new_row = {APIKeys.CONFIDENCE_AGE.value: distance_mean, APIKeys.CLASSIFIED_AGE.value: age_mean}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_age[regionkey] = region_mean_df

    return dict_age


def classify_gender(dict_all_info_knn):
    """
    simple classifier for gender prediction. Calculates the mode of the gender per region

    Args:
        dict_all_info_knn: dict {regionkey(str): region_df(uuid, distance, age, gender)}

    Returns:
        dict_gender: dict{regionkey(str): region_mean_df(mean_distance, gender_mode(0,1))}
    """
    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_GENDER.value, APIKeys.CLASSIFIED_GENDER.value])
        gender_list = region_df[Keys.GENDER.value].to_list()
        gender_mode = statistics.mode(gender_list)
        distance_list = region_df[Keys.DISTANCE.value].to_list()
        distance_mean = np.mean(distance_list)
        new_row = {APIKeys.CONFIDENCE_GENDER.value: distance_mean, APIKeys.CLASSIFIED_GENDER.value: gender_mode}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_gender[regionkey] = region_mean_df

    return dict_gender


def ensemble_age(age_dict):
    # TODO docstring
    age_list = [df[APIKeys.CLASSIFIED_AGE.value].iloc[0] for df in age_dict.values()]
    mean_age = np.mean(age_list)
    min_age = np.min(age_list)
    max_age = np.max(age_list)

    distance_list = [df[APIKeys.CONFIDENCE_AGE.value].iloc[0] for df in age_dict.values()]
    mean_distance = np.mean(distance_list)
    return mean_age, min_age, max_age, mean_distance


def ensemble_gender(gender_dict):
    # TODO: docstring
    gender_list = [df[APIKeys.CLASSIFIED_GENDER.value].iloc[0] for df in gender_dict.values()]
    mode_gender = statistics.mode(gender_list)

    distance_list = [df[APIKeys.CONFIDENCE_GENDER.value].iloc[0] for df in gender_dict.values()]
    mean_distance = np.mean(distance_list)
    return mode_gender, mean_distance


def ensemble_classifier(dict_age, dict_gender):
    """
    ensemble classifier of the prediction of age and gender from the individual hand regions forms.
    Returns dataframe for frontend

    Args:
        dict_age: dict{regionkey(str): region_mean_df(mean_distance, mean_age)}
        dict_gender: dict{regionkey(str): region_mean_df(mean_distance, gender_mode(0,1))}

    Returns:
        ensemble_df: pandasdataframe(classified_age(float),min_age(float),max_age(float), confidence_age(float),
        classified_gender(0,1), confidence_gender(float))
        0:female, 1:male
    """
    mean_age, min_age, max_age, mean_distance_age = ensemble_age(dict_age)
    mode_gender, mean_distance_gender = ensemble_gender(dict_gender)

    ensemble_df = pd.DataFrame(
        [
            {
                APIKeys.CLASSIFIED_AGE.value: mean_age,
                APIKeys.MIN_AGE.value: min_age,
                APIKeys.MAX_AGE.value: max_age,
                APIKeys.CONFIDENCE_AGE.value: mean_distance_age,
                APIKeys.CLASSIFIED_GENDER.value: mode_gender,
                APIKeys.CONFIDENCE_GENDER.value: mean_distance_gender,
            }
        ]
    )

    return ensemble_df
