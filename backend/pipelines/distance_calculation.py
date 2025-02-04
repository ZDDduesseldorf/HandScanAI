import numpy as np
from scipy.spatial import distance

from utils.key_enums import PipelineDictKeys as DictKeys
from utils.key_enums import HandRegions as RegionKeys
from .data_utils import region_embeddings_from_csv


# TODO: wird durch Vektordatenbank später ersetzt
def calculate_distance(dict_embedding: dict, k, embedding_csv_path):
    """
        Calculates cosine distances between the embedding of the new image and the embeddings of the data set and
        saves the results in a structured format.

    Args:
        dict_embedding: dict {regionkey(str) : embedding}
        k = number of nearest neighbours
        embedding_csv_path (Path): embedding_csv_path (Path): path to the regionkey_Embeddings.csv

    Returns:
        dict_dist: dict = {'Hand' : {'uuid': [56465, 1454514], 'distance': [0.1, 0.2], 'distance_ids_sorted' : [0,5]}}
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

    # für jede Region distanzen berechnen
    for regionkey, embedding in dict_embedding.items():
        # aufruf region_embeddings_from_csv(regionkey)
        list_uuid, list_embeddings = region_embeddings_from_csv(regionkey, embedding_csv_path)

        image_embedding = embedding
        list_dist = distance.cdist(image_embedding, list_embeddings, "cosine")
        list_dist = list_dist[0]
        # sortiert distanzen und speichert deren indexe ab
        list_sorted_dist = np.argsort(list_dist)
        list_sorted_dist = list_sorted_dist[:k]

        distance_dict[regionkey][DictKeys.UUID.value] = np.array(list_uuid)
        distance_dict[regionkey][DictKeys.DISTANCE.value] = np.array(list_dist)
        distance_dict[regionkey][DictKeys.DISTANCE_IDS_SORTED.value] = np.array(list_sorted_dist)

    return distance_dict
