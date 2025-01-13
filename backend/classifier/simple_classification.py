import numpy as np
import statistics
import pandas as pd

from pipelines.regions_utils import PipelineDataframeKeys as DfKeys


def classify_age(dict_all_info_knn):
    """
    simple classifier for age prediction. Calculates the mean of the age per region

    Args:
        dict_all_info_knn: dict {regionkey(str): region_df(uuid, distance, age, gender)}

    Returns:
        dict_age: dict{regionkey(str): region_mean_df(mean_distance, mean_age)}
    """
    dict_age = {}
    # TODO: PipelineDictKeys verwenden
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=["mean_distance", "mean_age"])
        age_list = region_df["age"].to_list()
        age_mean = np.mean(age_list)

        distance_list = region_df["distance"].to_list()
        distance_mean = np.mean(distance_list)
        new_row = {"mean_distance": distance_mean, "mean_age": age_mean}
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
    # TODO: PipelineDictKeys verwenden
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=["mean_distance", "mode_gender"])
        gender_list = region_df["gender"].to_list()
        gender_mode = statistics.mode(gender_list)
        distance_list = region_df["distance"].to_list()
        distance_mean = np.mean(distance_list)
        new_row = {"mean_distance": distance_mean, "mode_gender": gender_mode}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_gender[regionkey] = region_mean_df

    return dict_gender


def ensemble_age(age_dict):
    age_list = [df["mean_age"].iloc[0] for df in age_dict.values()]
    mean_age = np.mean(age_list)
    min_age = np.min(age_list)
    max_age = np.max(age_list)

    distance_list = [df["mean_distance"].iloc[0] for df in age_dict.values()]
    mean_distance = np.mean(distance_list)
    return mean_age, min_age, max_age, mean_distance


def ensemble_gender(gender_dict):
    gender_list = [df["mode_gender"].iloc[0] for df in gender_dict.values()]
    mode_gender = statistics.mode(gender_list)

    distance_list = [df["mean_distance"].iloc[0] for df in gender_dict.values()]
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
                DfKeys.CLASSIFIED_AGE.value: mean_age,
                DfKeys.MIN_AGE.value: min_age,
                DfKeys.MAX_AGE.value: max_age,
                DfKeys.CONFIDENCE_AGE.value: mean_distance_age,
                DfKeys.CLASSIFIED_GENDER.value: mode_gender,
                DfKeys.CONFIDENCE_GENDER.value: mean_distance_gender,
            }
        ]
    )

    return ensemble_df
