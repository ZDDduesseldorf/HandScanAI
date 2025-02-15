from __future__ import annotations
import subprocess
import typer
import uvicorn
import pipelines.initial_data_pipeline as initial_pipeline
from pipelines.initial_dataset_filter_pipeline import filter_11k_hands
from utils.logging_utils import setup_csv_logging
from hand_normalization.src import main as normalize
import cv2


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
    base_dataset_path = "app/media/BaseImages"
    region_dataset_path = "app/media/RegionImages"
    csv_folder_path = "app/media/csv"

    # Call the pipeline with paths
    initial_pipeline.run_initial_data_pipeline(base_dataset_path, region_dataset_path, csv_folder_path)


@cli.command("initial_dataset_filter")
def filter_11k_dataset():
    """Run filter_11k function."""
    # TODO: Pfade müssen vor Verwendung angepasst werden
    folder_path_initial_dataset = "path/to/image/folder"  # current dataset
    initial_csv_path = "path/to/csv"  # e.g. "J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\HandInfo.csv"
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
    # TODO: Pfade müssen vor Verwendung angepasst werden
    image_path = r"path/to/image/folder"
    region_dict = normalize.normalize_hand_image(image_path)
    image_list = list(region_dict.values())
    grid_image = normalize.draw_images_in_grid(image_list, rows=1, cols=7, image_size=(244, 244), bg_color=(23, 17, 13))

    cv2.imshow('Region Image Grid', grid_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cli()
