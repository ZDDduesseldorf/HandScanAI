import pipelines.initial_data_pipeline as initial_pipeline


def test_initial_data_pipeline(path_to_base_images, path_to_region_images):
    # run initial data pipeline once and check that returned dict has len 4 (4 uuid clusters)
    embeddings = initial_pipeline.run_initial_data_pipeline(
        base_dataset_path=path_to_base_images,
        region_dataset_path=path_to_region_images,
        # nur für manuelle Tests dieser Pfad, danach Dateien löschen
        csv_folder_path=path_to_base_images,
        save_images=False,
        save_csvs=False,
    )
    assert len(embeddings) == 4
