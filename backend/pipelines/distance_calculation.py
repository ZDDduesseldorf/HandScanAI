import numpy as np
from scipy.spatial import distance

from utils.key_enums import PipelineDictKeys as DictKeys
from utils.key_enums import HandRegions as RegionKeys
from .data_utils import region_embeddings_from_csv


# alternative to calculating the cosine similarity with Milvus is to calculate the cosine distance to the embeddings in the csv files


def calculate_cosine_distance(dict_embedding: dict, k: int, embedding_csv_path: str):
    """
    Calculates cosine distances between the embedding of the new image and the embeddings of the data set. The result of the distance function is a list containing the distance for each embedding pair.
    Determination of the k indexes with the smallest distance and save them in annother list.
    The list of the uuids, distances and indexes with the smallest distance are saved in a dictionary grouped by their region

    Args:
        dict_embedding (dict): dict {regionkey(str) : embedding}
        k (int): number of nearest neighbours
        embedding_csv_path (str): path to the regionkey_Embeddings.csv

    Returns:
        dict = {'Hand' : {'uuid': [56465, 1454514], 'distance': [0.1, 0.2], 'distance_ids_sorted' : [0,5]}}: list uuids, list distances, list indexex smallest distance grouped per region
    """

    distance_dict = {
        RegionKeys.HAND_0.value: {},
        RegionKeys.HANDBODY_1.value: {},
        RegionKeys.THUMB_2.value: {},
        RegionKeys.INDEXFINGER_3.value: {},
        RegionKeys.MIDDLEFINGER_4.value: {},
        RegionKeys.RINGFINGER_5.value: {},
        RegionKeys.LITTLEFINGER_6.value: {},
    }

    # Calculate distances for each region
    for regionkey, embedding in dict_embedding.items():
        list_uuid, list_embeddings = region_embeddings_from_csv(regionkey, embedding_csv_path)

        # convert lists to np arrays, reshape 1D arrays to 2D-arrays to be able to be used by cdist
        image_embedding = np.array(embedding).reshape(1, -1)

        list_dist = distance.cdist(image_embedding, list_embeddings, "cosine")
        list_dist = list_dist[0]
        # sorts distances and saves their indexes
        list_sorted_dist = np.argsort(list_dist)
        list_sorted_dist = list_sorted_dist[:k]

        distance_dict[regionkey][DictKeys.UUID.value] = np.array(list_uuid)
        distance_dict[regionkey][DictKeys.DISTANCE.value] = np.array(list_dist)
        distance_dict[regionkey][DictKeys.DISTANCE_IDS_SORTED.value] = np.array(list_sorted_dist)

    return distance_dict
