import pipelines.initial_data_pipeline as initial_pipeline
from pathlib import Path


def test_initial_data_pipeline(path_to_base_images, path_to_region_images):
    temp_base_dir = Path(__file__).resolve().parent.parent.parent
    # run initial data pipeline once and check that returned dict has len 4 (4 uuid clusters)
    folder_path_region = temp_base_dir / "app" / "media" / "RegionImages"
    embedding_csv_path = temp_base_dir / "app" / "media" / "csv"
    folder_path_base = temp_base_dir / "app" / "media" / "BaseImages"
    embeddings = initial_pipeline.run_initial_data_pipeline(
        base_dataset_path=folder_path_base,
        region_dataset_path=folder_path_region,
        # nur für manuelle Tests dieser Pfad, danach Dateien löschen
        csv_folder_path=embedding_csv_path,
        save_images=True,
        save_csvs=True,
    )
    assert len(embeddings) == 4
