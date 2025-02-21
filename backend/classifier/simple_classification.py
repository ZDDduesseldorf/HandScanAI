import numpy as np
import statistics
import pandas as pd


from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import PipelineAPIKeys as APIKeys


def classify_age(dict_all_info_knn: dict):
    """
    simple classifier for age prediction. Calculates the mean of the age per region

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        dict{regionkey(str): region_mean_df(mean_similarity, mean_age)}: dictionary that contains for each region the mean_similarity and mean_age
    """

    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_AGE.value, APIKeys.CLASSIFIED_AGE.value])
        age_list = region_df[Keys.AGE.value].to_list()
        age_mean = np.mean(age_list)

        similarity_list = region_df[Keys.SIMILARITY.value].to_list()
        similarity_mean = np.mean(similarity_list)
        new_row = {APIKeys.CONFIDENCE_AGE.value: similarity_mean, APIKeys.CLASSIFIED_AGE.value: age_mean}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_age[regionkey] = region_mean_df

    return dict_age


def classify_gender(dict_all_info_knn: dict):
    """
    simple classifier for gender prediction. Calculates the mode of the gender per region

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        dict{regionkey(str): region_mean_df(mean_similarity, gender_mode(0,1))}: dictionary that contains for each region the mean_similarity and mode_gender
    """

    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        region_mean_df = pd.DataFrame(columns=[APIKeys.CONFIDENCE_GENDER.value, APIKeys.CLASSIFIED_GENDER.value])
        gender_list = region_df[Keys.GENDER.value].to_list()
        gender_mode = statistics.mode(gender_list)
        similarity_list = region_df[Keys.SIMILARITY.value].to_list()
        similarity_mean = np.mean(similarity_list)
        new_row = {APIKeys.CONFIDENCE_GENDER.value: similarity_mean, APIKeys.CLASSIFIED_GENDER.value: gender_mode}
        region_mean_df = pd.concat([region_mean_df, pd.DataFrame([new_row])])
        dict_gender[regionkey] = region_mean_df

    return dict_gender


def confidence_gender(dict_all_info_knn: dict, predicted_gender: int):
    """
    Calculates the confidence of the predicted gender based on the gender of the nearest neighbours.
    Calculates the sum of neighbours with the same gender by the total number of neighbours

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}
        predicted_gender (int): classified gender from ensemble_gender (0: female, 1: male)

    Returns:
        confidence_gender (float)
    """
    list_gender = []
    for _, region_df in dict_all_info_knn.items():
        region_gender_list = region_df[Keys.GENDER.value].to_list()
        list_gender.extend(region_gender_list)

    number_correct_knn = list_gender.count(predicted_gender)
    number_knn = len(list_gender)
    confidence_gender = number_correct_knn / number_knn
    return confidence_gender


def ensemble_age(age_dict: dict):
    """
    Simple classifier for age prediction. Calculates the mean age, min age and max age from the age of the regions.
    Also calcualtes the mean of the similarities per region.

    Args:
        age_dict (dict): dict{regionkey(str): region_mean_df(mean_similarity, mean_age)}

    Returns:
        mean_age(float), min_age(float), max_age(float), mean_similarity(float)
    """
    age_list = [df[APIKeys.CLASSIFIED_AGE.value].iloc[0] for df in age_dict.values()]
    mean_age = np.mean(age_list)
    min_age = np.min(age_list)
    max_age = np.max(age_list)

    similarity_list = [df[APIKeys.CONFIDENCE_AGE.value].iloc[0] for df in age_dict.values()]
    mean_similarity = np.mean(similarity_list)
    return mean_age, min_age, max_age, mean_similarity


def ensemble_gender(gender_dict: dict):
    """
    Simple classifier for gender prediction. Calculates the mode gender from the gender of the regions.

    Args:
        dict_gender (dict): dict{regionkey(str): region_mean_df(mean_similarity, gender_mode(0,1))}

    Returns:
        mode_gender(int): 0: female, 1: male
    """
    gender_list = [df[APIKeys.CLASSIFIED_GENDER.value].iloc[0] for df in gender_dict.values()]
    mode_gender = statistics.mode(gender_list)

    return mode_gender


def simple_classifier(dict_all_info_knn: dict):
    """
    Simple classifier for predicting age and gender from the data of the nearest neighbours.
    First calculating age and gender per region and than calcuate the final result.
    Returns dataframe for frontend and dictionaries of the age and gender classification per region for logging.

    Args:
        dict_all_info_knn (dict): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        ensemble_df: pd.dataframe(classified_age(float),min_age(float),max_age(float), confidence_age(float),
        classified_gender(0,1), confidence_gender(float))
        dict_age: dict{regionkey(str): region_mean_df(mean_similarity, mean_age)}
        dict_gender: dict{regionkey(str): region_mean_df(mean_similarity, gender_mode(0,1))}
        0:female, 1:male
    """

    dict_age = classify_age(dict_all_info_knn)
    dict_gender = classify_gender(dict_all_info_knn)

    mean_age, min_age, max_age, mean_similarity_age = ensemble_age(dict_age)
    mode_gender = ensemble_gender(dict_gender)
    gender_confidence = confidence_gender(dict_all_info_knn, mode_gender)

    ensemble_df = pd.DataFrame(
        [
            {
                APIKeys.CLASSIFIED_AGE.value: mean_age,
                APIKeys.MIN_AGE.value: min_age,
                APIKeys.MAX_AGE.value: max_age,
                APIKeys.CONFIDENCE_AGE.value: mean_similarity_age,
                APIKeys.CLASSIFIED_GENDER.value: mode_gender,
                APIKeys.CONFIDENCE_GENDER.value: gender_confidence,
            }
        ]
    )

    return ensemble_df, dict_age, dict_gender
