from __future__ import annotations
import subprocess
import typer
import uvicorn
import pipelines.initial_data_pipeline as initial_pipeline
from pipelines.initial_dataset_filter_pipeline import filter_11k_hands
from utils.logging_utils import setup_csv_logging
from hand_normalization.src import main as normalize
import cv2
from pathlib import Path

cli = typer.Typer()


@cli.command("runserver")
def run_server(
    port: int = 8000,
    host: str = "localhost",
    log_level: str = "debug",
    reload: bool = True,
):
    """Run the API development server (uvicorn)."""
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command("format")
def format_code():
    """Format the code using ruff."""
    try:
        subprocess.run(
            [
                "ruff",
                "format",
                "app",
                "embeddings",
                "hand_normalization",
                "knn",
                "lib",
                "pipelines",
                "tests",
                "validation",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        typer.echo("Please fix the errors before committing.")
    finally:
        subprocess.run(["ruff", "clean"], check=True)


@cli.command("check")
def check_code():
    """Check the code using ruff."""
    try:
        subprocess.run(
            [
                "ruff",
                "check",
                "app",
                "embeddings",
                "hand_normalization",
                "knn",
                "lib",
                "pipelines",
                "tests",
                "validation",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        typer.echo("Please fix the errors before committing.")
    finally:
        subprocess.run(["ruff", "clean"], check=True)


@cli.command("test")
def run_tests():
    """Run the tests using pytest."""
    subprocess.run(["pytest", "tests"], check=True)


@cli.command("initial_data_pipeline")
def run_initial_data_pipeline():
    """Run the initial data pipeline."""
    # TODO: Set correct paths and flags before running the pipeline
    temp_base_dir = Path(__file__).resolve().parent
    base_dataset_path = temp_base_dir / "path/to/baseImages"  # e.g. temp_base_dir / "app" / "media" / "BaseImages"
    region_dataset_path = temp_base_dir / "path/to/regionImages"  # e.g.temp_base_dir / "app" / "media" / "RegionImages"
    csv_folder_path = temp_base_dir / "path/to/csvFolder"  # temp_base_dir / "app" / "media" / "csv"

    # Call the pipeline with paths
    initial_pipeline.run_initial_data_pipeline(
        base_dataset_path,
        region_dataset_path,
        csv_folder_path,
        normalize=False,
        save_images=False,
        save_csvs=True,
        save_milvus=True,
    )


@cli.command("initial_dataset_filter")
def filter_11k_dataset():
    """Run filter_11k function."""
    # TODO: Set correct paths before running the pipeline (ideally build via os.path or pathlib.Path, for example see function run_initial_data_pipeline)
    folder_path_initial_dataset = "path/to/image/folder"  # current dataset
    initial_csv_path = "path/to/csv"  # e.g. "path\to\HandInfo.csv"
    filtered_dataset_path = ""  # e.g. "NewDataset" or "BaseDataset"
    new_csv_path = "CSV_filtered.csv"
    filter_11k_hands(folder_path_initial_dataset, initial_csv_path, filtered_dataset_path, new_csv_path)


@cli.command("setup_csv_logging")
def initial_setup_csv_logging():
    """Run the setup csv-logging funktion."""
    setup_csv_logging()


@cli.command("normalisation_visual_test")
def normalisation_visual_test():
    """Run the a visual test of the normalize_hand_image() function"""
    # TODO: Set correct paths before using the function
    image_path = r"path/to/image/folder"
    region_dict = normalize.normalize_hand_image(image_path)
    image_list = list(region_dict.values())
    grid_image = normalize.draw_images_in_grid(image_list, rows=1, cols=7, image_size=(244, 244), bg_color=(23, 17, 13))

    cv2.imshow("Region Image Grid", grid_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cli()
