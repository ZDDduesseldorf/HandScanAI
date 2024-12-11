import pytest
from pathlib import Path

from pipelines.inference_pipeline import run_inference_pipeline, get_image_path
from pipelines.regions_utils import PipelineDictKeys as Keys


# TODO: Test ohne absoluten Pfad
# TODO: Test in utils?
# def test_image_path():
# image_path = Path(
# "C:/Users/leamu/Documents/1_uni/Medieninformatik/HandScanAI/git/HandScanAI/backend/tests/data/TestBaseDataset/514f53d0-6aab-4da1-b929-8f1dc0817289.jpg"
# )
# temp_base_dir = Path(__file__).resolve().parent.parent.parent
# calculate_image_path = get_image_path(temp_base_dir, "514f53d0-6aab-4da1-b929-8f1dc0817289")
# print(calculate_image_path)
# assert image_path == calculate_image_path


def test_run_inference_pipeline():
    uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    dict_embedding = run_inference_pipeline(uuid)
    print(dict_embedding)
    embeddings = dict_embedding[Keys.EMBEDDINGS.value]
    assert len(dict_embedding) == 2
    assert len(embeddings) == 7
