import pipelines.initial_data_pipeline as initial_pipeline


def test_initial_data_pipeline(path_to_base_images, path_to_region_images):
    # run initial data pipeline once and check that returned dict has len 2 (2 uuid clusters)
    embeddings = initial_pipeline.run_initial_data_pipeline(
        base_dataset_path=path_to_base_images,
        region_dataset_path=path_to_region_images,
        filter_initial_dataset=False,
        save_results_in_temp_folders=False,
    )
    assert len(embeddings) == 4
