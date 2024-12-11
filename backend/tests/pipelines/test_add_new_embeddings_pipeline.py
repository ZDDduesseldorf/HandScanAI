import pytest

from pipelines.add_new_embeddings_pipeline import run_add_new_embeddings_pipeline
from pipelines.regions_utils import PipelineDictKeys as Keys


def test_add_new_embeddings_pipeline():
    uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    dict_embedding = run_add_new_embeddings_pipeline(uuid)
    assert len(dict_embedding) == 7
