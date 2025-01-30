from collections import defaultdict

from pipelines.datasets import DatasetRegionClusters, ImagePathDataset
from utils.regions_utils import PipelineDictKeys, HandRegions

from embeddings import embeddings_utils

###########################################################
######### TESTS FOR DATASET IMAGE_PATH


# def test_if_loads_image_paths_correctly(path_to_base_images):
#     uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
#     dataset = ImagePathDataset(path_to_base_images)
#     # expect to load 1 image
#     assert len(dataset) == 4
#     # expect it to be a dict and to have the correct uuid
#     assert dataset[0][PipelineDictKeys.UUID.value] == uuid


###########################################################
######### TESTS FOR DATASET REGION_CLUSTERS


def test_correct_clusters(path_to_region_images):
    dataset = DatasetRegionClusters(path_to_region_images)
    # expected to load two clusters from testdata
    assert len(dataset) == 4


def test_correct_cluster_structure(path_to_region_images):
    dataset = DatasetRegionClusters(path_to_region_images)

    for cluster in dataset:
        # espect correct structure of clusters
        assert type(cluster[PipelineDictKeys.UUID.value]) is str
        assert type(cluster[PipelineDictKeys.IMAGE_PATHS_INITIAL.value]) is defaultdict
        assert len(cluster[PipelineDictKeys.IMAGE_PATHS_INITIAL.value]) == 7


def test_dataset_with_embeddings_calculation(path_to_region_images):
    dataset = DatasetRegionClusters(path_to_region_images)

    for cluster in dataset:
        test_embeddings = embeddings_utils.calculate_embeddings_from_path_dict(
            cluster[PipelineDictKeys.IMAGE_PATHS_INITIAL.value]
        )

        # expect 7 items in embeddings-dict
        assert type(test_embeddings) is dict
        assert len(test_embeddings) == 7
        # expect embeddings to have correct dimensions
        assert test_embeddings[HandRegions.HAND_0.value].shape[1] == 1024
