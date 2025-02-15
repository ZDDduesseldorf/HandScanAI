from __future__ import annotations
import subprocess
import typer
import uvicorn
import pipelines.initial_data_pipeline as initial_pipeline
from pipelines.initial_dataset_filter_pipeline import filter_11k_hands
from utils.logging_utils import setup_csv_logging
from hand_normalization.src import main as normalize
from pathlib import Path
import zipfile
from datetime import datetime
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
    initial_pipeline.run_initial_data_pipeline()


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


BACKUP_DIR = Path("backup")
BACKUP_FOLDERS = [Path("volumes"), Path("logs"), Path("app/media")]

@cli.command("create_backup")
def create_backup():
    """Create a backup of the volumes, logs, and media folders."""
    typer.echo("Creating backup...")

    try:
        # Generate timestamp and define backup file
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        BACKUP_DIR.mkdir(exist_ok=True)
        backup_zip_path = BACKUP_DIR / f"backup_{date_str}.zip"

        # Create ZIP file and preserve folder structure
        with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            for folder in BACKUP_FOLDERS:
                if folder.exists():
                    for file_path in folder.rglob("*"):
                        if file_path.is_file():
                            # Preserve exact path inside ZIP (app/media stays as "app/media")
                            backup_zip.write(file_path, file_path.relative_to(Path(".")))

        typer.echo(f"Backup successfully created at {backup_zip_path}")

    except Exception as e:
        typer.echo(f"Error creating backup: {e}", err=True)

    finally:
        if backup_zip_path.exists():
            typer.echo(f"Backup file saved: {backup_zip_path}")
        else:
            typer.echo("Backup failed. No file was created.", err=True)


@cli.command("restore_backup")
def restore_backup(backup_file: str):
    """Restore a backup by wiping old data and extracting from a ZIP file."""
    
    backup_path = BACKUP_DIR / backup_file

    if not backup_path.exists():
        typer.echo(f"Error: Backup file {backup_path} not found.", err=True)
        typer.Exit(1)

    typer.echo("WARNING: This will delete existing data and restore from the backup!")
    typer.confirm("Are you sure you want to continue?", abort=True)

    try:
        typer.echo("Wiping old data...")
        for folder in BACKUP_FOLDERS:
            if folder.exists():
                for file_path in folder.rglob("*"):
                    if file_path.is_file():
                        file_path.unlink()  # Delete file
                for subfolder in sorted(folder.glob("**/*"), reverse=True):
                    if subfolder.is_dir():
                        subfolder.rmdir()  # Remove empty folders
                folder.rmdir()  # Finally, remove the main directory

        typer.echo(f"Extracting backup from {backup_path}...")
        with zipfile.ZipFile(backup_path, 'r') as backup_zip:
            backup_zip.extractall(Path("."))  # Restore to current directory

        typer.echo("Backup successfully restored!")

    except Exception as e:
        typer.echo(f"Error restoring backup: {e}", err=True)
        typer.Exit(1)

if __name__ == "__main__":
    cli()
