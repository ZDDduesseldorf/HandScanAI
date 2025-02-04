from pipelines.add_new_embeddings_pipeline import run_add_new_embeddings_pipeline
from utils.key_enums import PipelineAPIKeys


def test_add_new_embeddings_pipeline():
    uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    ground_truth_data = {
        PipelineAPIKeys.REAL_AGE.value: 100,
        PipelineAPIKeys.REAL_GENDER.value: 0,
    }
    saved = run_add_new_embeddings_pipeline(uuid, ground_truth_data, testing=True)
    assert saved
