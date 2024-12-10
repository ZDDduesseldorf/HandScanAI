from pathlib import Path
import os

import pipelines.initial_data_pipeline as initial_pipeline


def test_initial_data_pipeline():
    # temp_base_dir geht bis backend
    temp_base_dir = Path(__file__).resolve().parent.parent
    print(temp_base_dir)
    base_dataset_path = temp_base_dir / "data" / "TestBaseDataset"
    region_dataset_path = temp_base_dir / "data" / "TestRegionDataset"

    embeddings = initial_pipeline.run_initial_data_pipeline(
        base_dataset_path=base_dataset_path,
        region_dataset_path=region_dataset_path,
        filter_initial_dataset=False,
        save_results_in_temp_folders=False,
    )
    assert len(embeddings) == 2
