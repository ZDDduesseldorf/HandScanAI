import pandas as pd

from utils.key_enums import PipelineDictKeys as DictKeys
from utils.key_enums import HandRegions as RegionKeys


def region_embeddings_from_csv(regionkey: str, embedding_csv_path: str):
    """
    reads the data from the regionkey_embeddings.csv and saves all uuids and all embeddings in seperated lists.

    Args:
        regionkey (str): name of the region
        embedding_csv_path (str): path to the regionkey_Embeddings.csv

    Returns:
        list_uuid (list): contains all uuids
        list_embedding (list): contains all embeddings

    Example:
        region_embeddings_from_csv("Hand", "C:\\HandScanAI\\backend\\app\\media\\csv\\Hand_Embeddings.csv")
    """

    name_csv = regionkey + "_Embeddings.csv"
    path_to_embeddings_csv = embedding_csv_path / name_csv
    embeddings_df = pd.read_csv(path_to_embeddings_csv, sep=",")
    embeddings_df["Embedding"] = embeddings_df["Embedding"].apply(
        lambda s: [float(x.strip(" []")) for x in s.split(",")]
    )
    list_uuid = embeddings_df["UUID"].tolist()
    list_embedding = embeddings_df["Embedding"].tolist()

    return list_uuid, list_embedding


def map_gender_string_to_int(df: pd.DataFrame):
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


def map_gender_int_to_string(int_gender: int):
    """
    Map gender numerical values in string falues
    0 mapped to 'female'
    1 mapped to 'male'

    Args:
        int_gender (int): gender als numeric value

    Returns:
        str: gender as string value

    Example:
        map_gender_int_to_string(0)
    """
    map_gender = {"0": "female", "1": "male"}
    return map_gender[str(int_gender)]


def build_info_knn_from_milvus(metadata_csv_path: str, knn_results: dict):
    """
    Supplement the results of the k-nearest neighbour search with Mivlus with additional metadata (age and gender) from a CSV file.
    Each region is mapped to a DataFrame containing the combined information.

    Args:
        metadata_csv_path (str): Path to the CSV file containing metadata. Must include 'uuid', 'age', and 'gender'.
        knn_results (Dict[str, List[Dict[str, Any]]]): Dictionary of k-NN results grouped by region.

    Returns:
        Dict[str, pd.DataFrame], {regionkey(str): region_df(uuid, similarity, age, gender)}: A dictionary mapping each region to a DataFrame with 'uuid', 'similarity', 'age', 'gender'.
    """
    dict_all_info_knn = {}

    metadata_df = pd.read_csv(metadata_csv_path, sep=",")
    metadata_df = map_gender_string_to_int(metadata_df)

    for region, knn_list in knn_results.items():
        region_df = pd.DataFrame(
            columns=[DictKeys.UUID.value, DictKeys.SIMILARITY.value, DictKeys.AGE.value, DictKeys.GENDER.value]
        )
        for hit in knn_list:
            uuid = hit.get(DictKeys.UUID.value)
            similarity = hit.get(DictKeys.SIMILARITY.value)

            row = metadata_df.loc[metadata_df[DictKeys.UUID.value] == uuid]
            if not row.empty:
                age = row[DictKeys.AGE.value].iloc[0]
                gender = row[DictKeys.GENDER.value].iloc[0]
            else:
                age = None
                gender = None

            new_row = {
                DictKeys.UUID.value: uuid,
                DictKeys.SIMILARITY.value: similarity,
                DictKeys.AGE.value: age,
                DictKeys.GENDER.value: gender,
            }
            region_df = pd.concat([region_df, pd.DataFrame([new_row])], ignore_index=True)

        dict_all_info_knn[region] = region_df

    return dict_all_info_knn


def build_info_knn_from_csv(metadata_csv_path: str, dict_all_dist: dict):
    """
    Filtering the results of the distance calculation with the csv data to the k-nearest neighbours per region.
    Supplementing this data with information about the age and gender of the neighbours from metadata.
    Calculation of the similarity of the nearest neighbours based on the distance.

    Args:
        metadata_csv_path(str): path to the folder where the csvs are saved
        dict_all_dist:  {'Hand' : {'uuid': [56465, 1454514], 'distance': [0.1, 0.2], 'distance_ids_sorted' : [0,5]}} Dictonary of distance calcualtion result grouped by region

    Returns:
        dict_all_info_knn: {regionkey(str): region_df(uuid, similarity, age, gender)} A dictionary mapping each region to a DataFrame with 'uuid', 'similarity', 'age', 'gender'.

    Example:
        build_info_knn("C:\\HandScanAI\\backend\\app\\media\\csv", dict = {'Hand' : {'uuid': [56465, 1454514], 'distance': [0.1, 0.2], 'distance_ids_sorted' : [0,5]}})
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

    metadata_df = pd.read_csv(metadata_csv_path, sep=",")
    metadata_df = map_gender_string_to_int(metadata_df)

    for regionkey, dist_dict in dict_all_dist.items():
        region_df = pd.DataFrame(
            columns=[DictKeys.UUID.value, DictKeys.SIMILARITY.value, DictKeys.AGE.value, DictKeys.GENDER.value]
        )
        for index in dist_dict[DictKeys.DISTANCE_IDS_SORTED.value]:
            # read uuid and distance to the corresponding index
            uuid = dist_dict[DictKeys.UUID.value][index]
            dist = dist_dict[DictKeys.DISTANCE.value][index]
            similarity = 1 - dist
            row = metadata_df.loc[metadata_df[DictKeys.UUID.value] == uuid]
            # .iloc[0] necessary otherwise one-dimensional column is saved, only value from cell is required
            age = row[DictKeys.AGE.value].iloc[0]
            gender = row[DictKeys.GENDER.value].iloc[0]
            new_row = {
                DictKeys.UUID.value: uuid,
                DictKeys.SIMILARITY.value: similarity,
                DictKeys.AGE.value: age,
                DictKeys.GENDER.value: gender,
            }
            region_df = pd.concat([region_df, pd.DataFrame([new_row])])

        dict_all_info_knn[regionkey] = region_df

    return dict_all_info_knn


def find_most_similar_nearest_neighbours(dict_all_info_knn: dict):
    """
    From all the nearest neighbours in each region, n are selected that have the highest similarity and differ in uuid.
    Saving of region, uuid, age and gender in dataframe for transfer to frontend

    Args:
        dict_all_info_knn (dictionary): dict {regionkey(str): region_df(uuid, similarity, age, gender)}

    Returns:
        pd.Dataframe: (region, uuid, age, gender) with n rows
    """
    knn_info_df = pd.DataFrame(
        columns=[
            DictKeys.REGION.value,
            DictKeys.UUID.value,
            DictKeys.SIMILARITY.value,
            DictKeys.AGE.value,
            DictKeys.GENDER.value,
        ]
    )

    for regionkey, region_df in dict_all_info_knn.items():
        for _, row in region_df.iterrows():
            new_row = {
                DictKeys.REGION.value: regionkey,
                DictKeys.UUID.value: row[DictKeys.UUID.value],
                DictKeys.SIMILARITY.value: row[DictKeys.SIMILARITY.value],
                DictKeys.AGE.value: row[DictKeys.AGE.value],
                DictKeys.GENDER.value: row[DictKeys.GENDER.value],
            }
            knn_info_df = pd.concat([knn_info_df, pd.DataFrame([new_row])])

    knn_info_df = knn_info_df.sort_values(by=[DictKeys.SIMILARITY.value], ascending=False)
    knn_info_df = knn_info_df.drop_duplicates(subset=DictKeys.UUID.value)
    knn_info_df = knn_info_df.head(3)
    knn_info_df = knn_info_df.drop(DictKeys.SIMILARITY.value, axis=1)
    return knn_info_df
