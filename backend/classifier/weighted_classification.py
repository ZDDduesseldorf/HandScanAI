import pandas as pd
import numpy as np

from pipelines.regions_utils import PipelineAPIKeys as APIKeys
from pipelines.regions_utils import PipelineDictKeys as Keys


def weighted_mean(dataframe, value, weight):
    values = dataframe[value]
    dataframe["calculated_weight"] = 1 - dataframe[weight]
    weighted_mean_age = (values * dataframe["calculated_weight"]).sum() / dataframe["calculated_weight"].sum()

    std_dev_age = weighted_std_dev(values, dataframe["calculated_weight"], weighted_mean_age)
    # mittelwert der Distanzen
    distance_mean = np.mean(dataframe["calculated_weight"])
    # mittelwert beider Fehler

    max_age_range = 75 - 20
    confidence_age = ((1 - (std_dev_age / max_age_range)) + (1 - distance_mean)) / 2
    return weighted_mean_age, confidence_age


def weighted_std_dev(values, weights, weighted_mean):
    weighted_diff = weights * (values - weighted_mean) ** 2
    weighted_variance = np.sum(weighted_diff) / weights.sum()
    weighted_std_dev = np.sqrt(weighted_variance)
    return weighted_std_dev


def weighted_mode_confidence(dataframe, value, weight):
    dataframe["calculated_weight"] = 1 / dataframe[weight]
    weighted_sum = dataframe.groupby(value)["calculated_weight"].sum()

    predicted_value = weighted_sum.idxmax()

    total_weight = weighted_sum.sum()
    confidence = weighted_sum[predicted_value] / total_weight

    return predicted_value, confidence


def weighted_classify_age(dict_all_info_knn):
    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_AGE.value, APIKeys.CLASSIFIED_AGE.value])

        weighted_mean_age, confidence_age = weighted_mean(region_df, Keys.AGE.value, Keys.DISTANCE.value)

        new_row = {APIKeys.CONFIDENCE_AGE.value: confidence_age, APIKeys.CLASSIFIED_AGE.value: weighted_mean_age}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_age[regionkey] = region_mean_df

    return dict_age


def weighted_classify_gender(dict_all_info_knn):
    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_GENDER.value, APIKeys.CLASSIFIED_GENDER.value])

        weighted_mode_gender, confidence_gender = weighted_mode_confidence(
            region_df, Keys.GENDER.value, Keys.DISTANCE.value
        )
        new_row = {
            APIKeys.CONFIDENCE_GENDER.value: confidence_gender,
            APIKeys.CLASSIFIED_GENDER.value: weighted_mode_gender,
        }
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_gender[regionkey] = region_mean_df

    return dict_gender
