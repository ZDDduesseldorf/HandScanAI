import pandas as pd

from .regions_utils import PipelineDictKeys as DictKeys
from .regions_utils import HandRegions as RegionKeys
from embeddings.embeddings_utils import calculate_embeddings_from_path_dict
from .datasets import DatasetRegionClusters


# test funktion ohne csv aller embeddings
# TODO: nach Integration embeddings-csv kann diese Funktion gelöscht werden
def util_test_embeddings_calculate(temp_base_dir):
    region_dataset_path = temp_base_dir / "tests" / "data" / "TestRegionDataset"

    embeddings_dict = {
        RegionKeys.HAND_0.value: {},
        RegionKeys.HANDBODY_1.value: {},
        RegionKeys.THUMB_2.value: {},
        RegionKeys.INDEXFINGER_3.value: {},
        RegionKeys.MIDDLEFINGER_4.value: {},
        RegionKeys.RINGFINGER_5.value: {},
        RegionKeys.LITTLEFINGER_6.value: {},
    }

    dataset = DatasetRegionClusters(region_dataset_path)

    for image_path_regions_cluster in dataset:
        uuid = image_path_regions_cluster[DictKeys.UUID.value]
        embeddings_regions_dict = calculate_embeddings_from_path_dict(
            image_path_regions_cluster[DictKeys.IMAGE_PATHS_INITIAL.value]
        )

        for region_key, embedding in embeddings_regions_dict.items():
            embeddings_dict[region_key][uuid] = embedding

    return embeddings_dict


# TODO: erstellen
# def region_embeddings_from_csv (regionkey):
# pro regionkey in ordner pd.Dataframe csv laden
# uuid in liste
# embeddings in liste
# return list_uuid, list_embeddings


def map_gender(df):
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


# TODO: fix deprecation warnings
def build_info_knn(temp_base_dir, dict_all_dist: dict):
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
    # TODO: Pfad ändern
    metadata_path = temp_base_dir / "tests" / "data" / "csv" / "Test_Hands_filtered_metadata.csv"
    metadata_df = pd.read_csv(metadata_path, sep=",")
    metadata_df = map_gender(metadata_df)

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
