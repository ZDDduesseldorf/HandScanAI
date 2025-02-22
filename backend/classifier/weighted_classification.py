import pandas as pd
import numpy as np

from utils.key_enums import PipelineAPIKeys as APIKeys
from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import HandRegions


# weights per region for the ensemble classifier
ensemble_weight_dict_age = {
    HandRegions.HAND_0.value: 1,
    HandRegions.HANDBODY_1.value: 0.75,
    HandRegions.THUMB_2.value: 0.25,
    HandRegions.INDEXFINGER_3.value: 0.25,
    HandRegions.MIDDLEFINGER_4.value: 1,
    HandRegions.RINGFINGER_5.value: 0.5,
    HandRegions.LITTLEFINGER_6.value: 0.25,
}

ensemble_weight_dict_gender = {
    HandRegions.HAND_0.value: 1,
    HandRegions.HANDBODY_1.value: 1,
    HandRegions.THUMB_2.value: 1,
    HandRegions.INDEXFINGER_3.value: 1,
    HandRegions.MIDDLEFINGER_4.value: 1,
    HandRegions.RINGFINGER_5.value: 1,
    HandRegions.LITTLEFINGER_6.value: 1,
}


def weighted_classifier(
    dict_all_info_knn: dict[str, pd.DataFrame],
    ensemble_weight_dict_age: dict[str, float] = ensemble_weight_dict_age,
    ensemble_weight_dict_gender: dict[str, float] = ensemble_weight_dict_gender,
):
    """
    Weighted classifier for predicting age and gender from the data of the nearest neighbours with weights.
    First calculating age and gender per region and than calcuate the final result.
    Returns dataframe for Frontend.

    Args:
        dict_all_info_knn (dict[str, pd.DataFrame]): dict {regionkey(str): region_df(uuid, similarity, age, gender)}
        ensemble_weight_dict_age (dict[str, float], optional): dictionary with weights for each region for age classification. Defaults to ensemble_weight_dict_age.
        ensemble_weight_dict_gender (dict[str, float], optional): dictionary with weights for each region for gender classification. Defaults to ensemble_weight_dict_gender.

    Returns:
        ensemble_df: pandasdataframe(classified_age(float),min_age(float),max_age(float), confidence_age(float),
        classified_gender(0,1), confidence_gender(float))
        dict_age: dict{regionkey(str): region_mean_df(mean_similarity, mean_age)}
        dict_gender: dict{regionkey(str): region_mean_df(mean_similarity, gender_mode(0,1))}
        0:female, 1:male
    """

    # calculate weighted age and gender per region
    dict_age = weighted_classify_age(dict_all_info_knn)
    dict_gender = weighted_classify_gender(dict_all_info_knn)

    # calcuate predicted age, gender an their confidence
    weighted_mean_age = weighted_ensemble_age(dict_age, ensemble_weight_dict_age)
    lower_interval_age, upper_interval_age = confidence_intervall_age(dict_all_info_knn)
    confidence_age = 0  # currently not calculated
    weighted_mode_gender = weighted_ensemble_gender(dict_gender, ensemble_weight_dict_gender)
    weighted_confidence_gender = caculate_weighted_confidence_gender(dict_all_info_knn, weighted_mode_gender)

    # create dataframe for Frontend
    ensemble_df = pd.DataFrame(
        [
            {
                APIKeys.CLASSIFIED_AGE.value: weighted_mean_age,
                APIKeys.MIN_AGE.value: lower_interval_age,
                APIKeys.MAX_AGE.value: upper_interval_age,
                APIKeys.CONFIDENCE_AGE.value: confidence_age,
                APIKeys.CLASSIFIED_GENDER.value: weighted_mode_gender,
                APIKeys.CONFIDENCE_GENDER.value: weighted_confidence_gender,
            }
        ]
    )

    return ensemble_df, dict_age, dict_gender


def weighted_classify_age(dict_all_info_knn: dict):
    """
    weighted classifier for age prediction. Calculates the weighted mean of the age per region based on the similarity.

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        dict{regionkey(str): region_mean_df(confidence_age, weighted_mean_age)}: dictionary that contains for each region the confidence_age and weighted_mean_age

    """
    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        age_column = pd.to_numeric(region_df[Keys.AGE.value], errors="raise")
        region_df["calculated_weight"] = region_df[Keys.SIMILARITY.value]
        calculated_weight_column = region_df["calculated_weight"]

        weighted_mean_age_region = weighted_mean(calculated_weight_column, age_column)
        confidence_age = 0  # currently not calculated

        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_AGE.value, APIKeys.CLASSIFIED_AGE.value])
        new_row = {APIKeys.CONFIDENCE_AGE.value: confidence_age, APIKeys.CLASSIFIED_AGE.value: weighted_mean_age_region}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_age[regionkey] = region_mean_df

    return dict_age


def weighted_mean(weights: list | np.ndarray | pd.Series, values: list | np.ndarray | pd.Series):
    """
    calcualtes the weighted mean
    weighted_mean = sum(values[i] * weights[i]) / sum(weights)

    Args:
        weights (list  |  np.array  |  pd.Series): A list, a NumPy array or a Pandas serie with non-negative weight values.
        values (list  |  np.array  |  pd.Series): A list, a NumPy array or a Pandas series with numerical values to be averaged.

    Returns:
        weighted_mean_age(float): weighted mean
    """

    weighted_mean_age = np.average(values, weights=weights)
    return weighted_mean_age


def weighted_classify_gender(dict_all_info_knn: dict):
    """
    weighted classifier for gender prediction. Calculates the weighted mode of the gender per region

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        dict{regionkey(str): region_mean_df(gender_confidence, gender_mode(0,1))}: dictionary that contains for each region the gender_confidence and mode_gender

    """
    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_df["calculated_weight"] = region_df[Keys.SIMILARITY.value]
        weighted_mode_gender = weighted_mode(region_df, Keys.GENDER.value, "calculated_weight")
        gender_confidence = 0  # currently not calculated
        new_row = {
            APIKeys.CONFIDENCE_GENDER.value: gender_confidence,
            APIKeys.CLASSIFIED_GENDER.value: weighted_mode_gender,
        }
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_GENDER.value, APIKeys.CLASSIFIED_GENDER.value])
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_gender[regionkey] = region_mean_df

    return dict_gender


def weighted_mode(dataframe: pd.DataFrame, value: str, weight: str):
    """
    Calculates the weighted mode (most common value based on weights)
    Args:
        dataframe (pd.DataFrame): a pandas dataframe with the data to be analysed
        value (str): name of the column with the values
        weight (str): name of the column with the weights

    Returns:
        weighted_mode(int): 0: female, 1: male
    """
    weighted_sum = dataframe.groupby(value)[weight].sum()
    weighted_mode = weighted_sum.idxmax()
    return weighted_mode


def confidence_intervall_age(dict_all_info_knn: dict):
    """
    calculates the lower and upper edge of the data interval. 5% of the data is cut off at the top and bottom.

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        lower_quantile (int), upper_quantile(int)
    """
    list_age = []
    for _, region_df in dict_all_info_knn.items():
        region_age_list = region_df[Keys.AGE.value].to_list()
        list_age.extend(region_age_list)

    lower_quantile = np.percentile(list_age, 5)
    upper_quantile = np.percentile(list_age, 95)

    return lower_quantile, upper_quantile


def caculate_weighted_confidence_gender(dict_all_info_knn, predicted_gender):
    """
    Calculates the weighted confidence of the predicted gender based on the weights of the gender of the nearest neighbours.
    Calculates the confidence by the ratio of the sum of the weights of the neighbours with the same gender as the predicted gender to that of all weights

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}
        predicted_gender (int): classified gender from ensemble_gender (0: female, 1: male)

    Returns:
        weighted_confidence_gender (float)
    """
    weights_correct_knn = 0
    sum_weights = 0
    for _, region_df in dict_all_info_knn.items():
        region_df["calculated_weight"] = region_df[Keys.SIMILARITY.value]
        weighted_sum = region_df.groupby(Keys.GENDER.value)["calculated_weight"].sum()
        # Ensure that both values (0 and 1) are included
        weighted_sum = weighted_sum.reindex([0, 1], fill_value=0)
        weight_predicted_gender = weighted_sum.loc[predicted_gender]
        weights_correct_knn += weight_predicted_gender
        sum_weights_region = region_df["calculated_weight"].sum()
        sum_weights += sum_weights_region

    weighted_confidence_gender = weights_correct_knn / sum_weights

    return weighted_confidence_gender


def weighted_ensemble_age(dict_age: dict, weight_dict: dict):
    """
    Weighted ensemble classifier for age prediction. Calculates the weighted mean age from the age of the regions.

    Args:
        dict_age (dict): dict{regionkey(str): region_mean_df(mean_similarity, mean_age)}
        weight_dict (dict): dict{regionkey(str): weight(float)}

    Returns:
        weighted_mean_age(float)

    """
    age_list = [df[APIKeys.CLASSIFIED_AGE.value].iloc[0] for df in dict_age.values()]
    weight_list = []
    for _, weight in weight_dict.items():
        weight_list.append(weight)

    weighted_mean_age = weighted_mean(weight_list, age_list)
    return weighted_mean_age


def weighted_ensemble_gender(dict_gender: dict, weight_dict: dict):
    """
    Weighted ensemble classifier for gender prediction. Calculates the weighted mode gender from the gender of the regions.

    Args:
        dict_gender (dict): dict{regionkey(str): region_mean_df(mean_similarity, mean_gender)}
        weight_dict (dict): dict{regionkey(str): weight(float)}

    Returns:
        weighted_mode_gender(int): [0: female, 1: male]
    """
    ensemble_gender_df = pd.DataFrame(columns=[APIKeys.CLASSIFIED_GENDER.value, "calculated_weight"])
    for regionkey, region_df in dict_gender.items():
        new_row = {
            APIKeys.CLASSIFIED_GENDER.value: region_df.loc[0, APIKeys.CLASSIFIED_GENDER.value],
            "calculated_weight": weight_dict[regionkey],
        }
        ensemble_gender_df = pd.concat([ensemble_gender_df, pd.DataFrame([new_row])])
    weighted_mode_gender = weighted_mode(ensemble_gender_df, APIKeys.CLASSIFIED_GENDER.value, "calculated_weight")
    return weighted_mode_gender
