from pathlib import Path
from pipelines.initial_dataset_filter_pipeline import filter_11k_hands


def test_filter_11k_hands():
    tem_base_dir = Path(__file__).resolve().parent.parent.parent
    folder_path = tem_base_dir / "app" / "media" / "Hands"
    csv_path = tem_base_dir / "app" / "media" / "Hands" / "Handinfo.csv"
    new_dataset_path = tem_base_dir / "app" / "media" / "filter_dataset"
    new_csv_path = tem_base_dir / "app" / "media" / "filter_dataset" / "Metadata_filter.csv"
    filter_11k_hands(folder_path, csv_path, new_dataset_path, new_csv_path)
