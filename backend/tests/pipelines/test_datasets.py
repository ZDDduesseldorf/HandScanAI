import pytest

from pipelines.datasets import DatasetRegions
from pipelines.hand_regions import hand_region_order

from embeddings import embeddings_utils
from embeddings import models_utils

######### TESTS FOR DATASET REGIONS


def test_correct_clusters(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=True)
    # expected to load two clusters from testdata
    assert len(dataset) == 2


def test_correct_order_of_image_paths(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=True)
    # Iterate over the Dataset
    # for image_paths in dataset:
    #    print("Image Path:", image_paths)  # -> prints an array of all imagepaths with the same uuid each iteration
    for cluster in dataset:
        for i, region in enumerate(hand_region_order):
            assert region in cluster[i]


def test_correct_loading_of_single_images(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=False)
    assert len(dataset) == 14


def test_images_with_embeddings(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=True)

    for cluster in dataset:
        test_embeddings = embeddings_utils.calculate_embeddings_from_full_paths(cluster, models_utils.load_model())
        assert len(test_embeddings) == 7
        assert test_embeddings[0].shape[1] == 1024
