from collections import defaultdict

from pipelines.datasets import DatasetRegionClusters, ImagePathDataset
from utils.key_enums import PipelineDictKeys, HandRegions

from embeddings import embeddings_utils

###########################################################
######### TESTS FOR DATASET IMAGE_PATH


def test_correct_image_path_dict_structure(path_to_base_images):
    dataset = ImagePathDataset(path_to_base_images)
    # expect to load 4 images from folder TestBaseDataset
    assert len(dataset) == 4
    # expect it to be a dict
    assert type(dataset[0]) is dict
    # expect dict to have a uuid and an image_path both of type string
    assert type(dataset[0][PipelineDictKeys.UUID.value]) is str
    assert type(dataset[0][PipelineDictKeys.IMAGE_PATH.value]) is str


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
