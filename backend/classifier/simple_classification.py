import numpy as np
import statistics


def classify_age(dict_all_info_knn):
    """
    simple classifier for age prediction. Calculates the mean of the age per region

    Args:
        dict_all_info_knn: dict {regionkey(str): region_df(uuid, distance, age, gender)}

    Returns:
        dict_age: dict{regionkey(str): age_mean(float)}
    """
    # return dict {'hand' : mean_age}
    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        age_list = region_df["age"].to_list()
        age_mean = np.mean(age_list)
        dict_age[regionkey] = age_mean

    return dict_age


def classify_gender(dict_all_info_knn):
    """
    simple classifier for gender prediction. Calculates the mode of the gender per region

    Args:
        dict_all_info_knn: dict {regionkey(str): region_df(uuid, distance, age, gender)}

    Returns:
        dict_gender: dict{regionkey(str): gender_mode(0,1)}
    """
    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        gender_list = region_df["gender"].to_list()
        gender_mode = statistics.mode(gender_list)
        dict_gender[regionkey] = gender_mode

    return dict_gender
