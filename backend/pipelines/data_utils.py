import pandas as pd

from .regions_utils import PipelineDictKeys as DictKeys
from .regions_utils import HandRegions as RegionKeys


def region_embeddings_from_csv(regionkey, embedding_csv_path):
    name_csv = regionkey + "_Embeddings.csv"
    path_to_embeddings_csv = embedding_csv_path / name_csv
    embeddings_df = pd.read_csv(path_to_embeddings_csv, sep=",")
    embeddings_df["Embedding"] = embeddings_df["Embedding"].apply(
        lambda s: [float(x.strip(" []")) for x in s.split(",")]
    )
    list_uuid = embeddings_df["UUID"].tolist()
    list_embedding = embeddings_df["Embedding"].tolist()

    return list_uuid, list_embedding


def map_gender_string_to_int(df):
    """
        Map gender values in a DataFrame to numerical values
        'female' mapped to 0
        'male' mapped to 1

    Args:
        df (pd.DataFrame): The input DataFrame containing a "gender" column with values as strings ("female" or "male").

    Returns:
        df: pandas dataframe with replaced values


    """
    map_gender = {"female": 0, "male": 1}
    df = df.replace({"gender": map_gender}).infer_objects(copy=False)
    return df


def build_info_knn(metadata_csv_path, dict_all_dist: dict):
    """
    Query of gender and age for knn of the image from csv.
    Dictation of a dict that contains the k nearest neighbours with uuid, dist, age and gender

    Args:
        temp_base_dir(Path): The base directory. Typically derived from the current file's location.
        dict_all_dist:  {'Hand' : {'uuid': [56465, 1454514], 'distance': [0.1, 0.2], 'distance_ids_sorted' : [0,5]}}

    Returns:
        dict_all_info_knn: {regionkey(str): region_df(uuid, dist, age, gender)}

    """
    dict_all_info_knn = {
        RegionKeys.HAND_0.value: {},
        RegionKeys.HANDBODY_1.value: {},
        RegionKeys.THUMB_2.value: {},
        RegionKeys.INDEXFINGER_3.value: {},
        RegionKeys.MIDDLEFINGER_4.value: {},
        RegionKeys.RINGFINGER_5.value: {},
        RegionKeys.LITTLEFINGER_6.value: {},
    }

    # TODO: Abfrage aus MongoDB?
    metadata_df = pd.read_csv(metadata_csv_path, sep=",")
    metadata_df = map_gender_string_to_int(metadata_df)

    for regionkey, dist_dict in dict_all_dist.items():
        region_df = pd.DataFrame(columns=[DictKeys.UUID.value, "distance", "age", "gender"])
        for index in dist_dict["distance_ids_sorted"]:
            uuid = dist_dict[DictKeys.UUID.value][index]
            dist = dist_dict["distance"][index]
            row = metadata_df.loc[metadata_df["uuid"] == uuid]
            # .iloc[0] notwendig sonst wird eindimensionale column gespeichert, nur Wert aus Zelle wird benötigt
            age = row["age"].iloc[0]
            gender = row["gender"].iloc[0]
            new_row = {DictKeys.UUID.value: uuid, "distance": dist, "age": age, "gender": gender}
            region_df = pd.concat([region_df, pd.DataFrame([new_row])])

        dict_all_info_knn[regionkey] = region_df

    return dict_all_info_knn
