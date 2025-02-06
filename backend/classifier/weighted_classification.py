import pandas as pd
import numpy as np

from utils.key_enums import PipelineAPIKeys as APIKeys
from utils.key_enums import PipelineDictKeys as Keys
from classifier.simple_classification import ensemble_age, ensemble_gender, confidence_gender


# TODO: was ist gutes gewicht?


def weighted_classify_age(dict_all_info_knn):
    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_AGE.value, APIKeys.CLASSIFIED_AGE.value])

        weighted_mean_age = weighted_mean(region_df, Keys.AGE.value, Keys.DISTANCE.value)

        # TODO: brauchen wir diesen Wert noch?
        confidence_age = 0  # aktuell nicht berechnet
        new_row = {APIKeys.CONFIDENCE_AGE.value: confidence_age, APIKeys.CLASSIFIED_AGE.value: weighted_mean_age}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_age[regionkey] = region_mean_df

    return dict_age


def weighted_mean(dataframe, value, weight):
    values = dataframe[value]
    dataframe["calculated_weight"] = 1 - dataframe[weight]  # TODO: oder 1/?
    weighted_mean_age = np.average(values, weights=dataframe["calculated_weight"])

    return weighted_mean_age


def weighted_classify_gender(dict_all_info_knn):
    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_GENDER.value, APIKeys.CLASSIFIED_GENDER.value])

        weighted_mode_gender = weighted_mode(region_df, Keys.GENDER.value, Keys.DISTANCE.value)
        # TODO: brauchen wir diesen Wert noch?
        gender_confidence = 0  # aktuell nicht berechnet
        new_row = {
            APIKeys.CONFIDENCE_GENDER.value: gender_confidence,
            APIKeys.CLASSIFIED_GENDER.value: weighted_mode_gender,
        }
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_gender[regionkey] = region_mean_df

    return dict_gender


def weighted_mode(dataframe, value, weight):
    dataframe["calculated_weight"] = 1 - dataframe[weight]  # TODO: oder 1/?
    weighted_sum = dataframe.groupby(value)["calculated_weight"].sum()

    predicted_value = weighted_sum.idxmax()
    return predicted_value


def confidenceintervall_age(dict_all_info_knn):
    # TODO: konfidenz vielleicht etwas irreführend, Interquartilsbereich  vielleicht etwas besser
    list_age = []
    for regionkey, region_df in dict_all_info_knn.items():
        region_age_list = region_df[Keys.AGE.value].to_list()
        list_age.extend(region_age_list)

    lower_quantile = np.percentile(list_age, 5)
    upper_quantile = np.percentile(list_age, 95)

    return lower_quantile, upper_quantile


def weighted_confidence_gender(dict_all_info_knn, predicted_gender):
    # TODO prüfen ob dies so sinnvoll ist
    weights_correct_knn = 0
    sum_weights = 0
    for regionkey, region_df in dict_all_info_knn.items():
        region_df["calculated_weight"] = 1 - region_df[Keys.DISTANCE.value]  # TODO: oder 1/?
        weighted_sum = region_df.groupby(Keys.GENDER.value)["calculated_weight"].sum()
        weight_predicted_gender = weighted_sum.loc[predicted_gender]
        weights_correct_knn += weight_predicted_gender
        sum_weights_region = region_df["calculated_weight"].sum()
        sum_weights += sum_weights_region

    confidence_gender = weights_correct_knn / sum_weights

    return confidence_gender


def weighted_classfier(dict_all_info_knn):
    dict_age = weighted_classify_age(dict_all_info_knn)
    dict_gender = weighted_classify_gender(dict_all_info_knn)

    # TODO: durch weighted ensemble ersetzen
    mean_age, min_age, max_age, mean_distance_age = ensemble_age(dict_age)
    lower_interval_age, upper_interval_age = confidenceintervall_age(dict_all_info_knn)
    mode_gender = ensemble_gender(dict_gender)
    gender_confidence = weighted_confidence_gender(dict_all_info_knn, mode_gender)

    ensemble_df = pd.DataFrame(
        [
            {
                APIKeys.CLASSIFIED_AGE.value: mean_age,
                APIKeys.MIN_AGE.value: lower_interval_age,
                APIKeys.MAX_AGE.value: upper_interval_age,
                APIKeys.CONFIDENCE_AGE.value: mean_distance_age,
                APIKeys.CLASSIFIED_GENDER.value: mode_gender,
                APIKeys.CONFIDENCE_GENDER.value: gender_confidence,
            }
        ]
    )

    return ensemble_df, dict_age, dict_gender
