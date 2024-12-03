import pytest

from pipelines.datasets import DatasetRegions

from embeddings import embeddings_utils
from embeddings import models_utils


def test_correct_clusters(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=True)

    # expected to load two clusters from testdata
    assert len(dataset) == 2


def test_correct_loading_of_single_images(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=False)
    assert len(dataset) == 14


def test_images_with_embeddings(path_to_region_images):
    dataset = DatasetRegions(path_to_region_images, clustered_data=True)

    for cluster in dataset:
        test_embeddings = embeddings_utils.calculate_embeddings_from_full_paths(cluster, models_utils.load_model())
        assert len(test_embeddings) == 7
        assert test_embeddings[0].shape[1] == 1024
