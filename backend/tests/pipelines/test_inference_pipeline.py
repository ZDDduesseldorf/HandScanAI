from pipelines.inference_pipeline import run_inference_pipeline


def test_run_inference_pipeline():
    uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    classification_df, knn_info_df = run_inference_pipeline(uuid, testing=True, use_milvus=False)
    # column: index + 5 Parameter
    assert classification_df.shape == (1, 6)
    # 3 rows each with 4 columns
    assert knn_info_df.shape == (3, 4)
