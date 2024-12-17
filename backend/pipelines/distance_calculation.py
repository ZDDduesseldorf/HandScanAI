import numpy as np
from scipy.spatial import distance

from .regions_utils import PipelineDictKeys as DictKeys
from .regions_utils import HandRegions as RegionKeys


# TODO: wird durch Vektordatenbank später ersetzt
def calculate_distance(dict_embedding, dict_all_embeddings: dict, k):
    """
        Calculates cosine distances between the embedding of the new image and the embeddings of the data set and
        saves the results in a structured format.

    Args:
        dict_embedding: dict {regionkey(str) : embedding}
        dict_all_embeddings: dict{regionkey(str): {uuid:embedding}}

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

    # TODO: Anpassung an csv
    # für jede Region distanzen berechnen
    for regionkey, embedding_dict in dict_all_embeddings.items():
        # aufruf region_embeddings_from_csv(regionkey)
        list_uuid = []
        list_embeddings = []

        for uuid, embedding in embedding_dict.items():  # kann weg
            list_uuid.append(uuid)
            list_embeddings.append(embedding[0])
        image_embedding = dict_embedding[regionkey]
        list_dist = distance.cdist(image_embedding, list_embeddings, "cosine")
        list_dist = list_dist[0]
        # sortiert distanzen und speichert deren indexe ab
        list_sorted_dist = np.argsort(list_dist)
        list_sorted_dist = list_sorted_dist[:k]

        distance_dict[regionkey][DictKeys.UUID.value] = np.array(list_uuid)
        distance_dict[regionkey]["distance"] = np.array(list_dist)
        distance_dict[regionkey]["distance_ids_sorted"] = np.array(list_sorted_dist)

    return distance_dict
