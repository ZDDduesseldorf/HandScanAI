import pytest
from pathlib import Path

from pipelines.inference_pipeline import run_inference_pipeline, get_image_path


def test_image_path():
    image_path = Path("C:/Users/leamu/Documents/1_uni/Medieninformatik/HandScanAI/git/HandScanAI/backend/tests/data/TestImages/Hand_0000002.jpg")
    temp_base_dir = Path(__file__).resolve().parent.parent.parent
    calculate_image_path = get_image_path(temp_base_dir, "Hand_0000002")
    print(calculate_image_path)
    assert image_path == calculate_image_path

def test_run_inference_pipeline():
    uuid= "Hand_0000002"
    embedding = run_inference_pipeline(uuid)
    print(embedding)
    # calculate_embedding(image_tensor) -> tensor([[3.5176e-04, 3.8136e-03, 4.9482e-03,  ..., 2.5515e+00, 2.0205e-01,         4.0587e-01]])
    #prüft shape von tensor aus hand-normalization
    assert embedding.shape[1] == 1024
    
    


    