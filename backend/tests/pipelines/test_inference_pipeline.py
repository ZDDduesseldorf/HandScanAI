from pipelines.inference_pipeline import run_inference_pipeline


# TODO: Test ohne absoluten Pfad
# TODO: Test in utils?
# def test_image_path():
# image_path = Path(
# "C:/Users/leamu/Documents/1_uni/Medieninformatik/HandScanAI/git/HandScanAI/backend/tests/data/
# TestBaseDataset/514f53d0-6aab-4da1-b929-8f1dc0817289.jpg"
# )
# temp_base_dir = Path(__file__).resolve().parent.parent.parent
# calculate_image_path = get_image_path(temp_base_dir, "514f53d0-6aab-4da1-b929-8f1dc0817289")
# print(calculate_image_path)
# assert image_path == calculate_image_path


def test_run_inference_pipeline():
    uuid = "514f53d0-6aab-4da1-b929-8f1dc0817289"
    classification_df = run_inference_pipeline(uuid, testing=False)
    # column: index + 5 Parameter
    assert classification_df.shape == (1, 6)
