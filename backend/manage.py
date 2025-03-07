from __future__ import annotations
import subprocess
import typer
import uvicorn
from embeddings.embeddings_utils import _default_cnn_model_, default_model_name
import pipelines.initial_data_pipeline as initial_pipeline
from pipelines.initial_dataset_filter_pipeline import filter_11k_hands
from utils.logging_utils import setup_csv_logging
from hand_normalization.src import main as normalize
from vectordb.milvus import drop_collection, milvus_collection_name
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
                "classifier",
                "embeddings",
                "hand_normalization",
                "lib",
                "pipelines",
                "tests",
                "utils",
                "validation",
                "vectordb",
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
                "classifier",
                "embeddings",
                "hand_normalization",
                "lib",
                "pipelines",
                "tests",
                "utils",
                "validation",
                "vectordb",
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


@cli.command("setup_new_project_data")
def setup_new_project_with_initial_data_pipeline():
    """
    Run the initial data pipeline to newly set up the project data.
    This function can be used to initially setup the project data for the first time or to wipe already existing embeddings and calculate them anew.
    Changing the flags, it is also possible to generate new RegionImages (will be explained in greater detail below).

    Should be used if project is setup newly on a device (due to slight differences in embeddings calculation per device,
    it is advised to calculate them new and not use embeddings calculated and saved by other devices).


    Prerequisites:
        You can use the function **as is** if you
        - copied the dataset's BaseImages into backend/app/media/BaseImages
        - copied the dataset's RegionImages into backend/app/media/RegionImages
        - created the folder backend/app/media/csv with the dataset's Metadata.csv (and no other csvs. Important, see explanation**)
        - want to calculate the RegionImages' embeddings and safe them in csv-files as well as the milvus vector-database in bulk as a initial setup.

    ** If Embeddings.csvs already exist there, optionally save them somewhere else and delete them from the folder to not mix in old data.
    If you want to add images in bulk to already existing data, please use `bulk_import_with_initial_data_pipeline` below.

    If all the requirements are met, use the manage.py command `setup_new_project_data` on the commandline (e.g. `python manage.py setup_new_project_data`).
    The function will
    - first delete any existing milvus collection with the default collection name
    - skip normalization of BaseImages because RegionImages already contains normalized images
    - calculate Embeddings for all images in RegionImages and
    - save them in csv-files as well as the newly created milvus vector-database with the default collection name.

    These embeddings will then be used as base data for the distance-calculation and classification in the inference-pipeline.
    The created dataset also provides the structure for later adding new images, their metadata and their embeddings one by one via add_new_embeddings_pipeline.

    It is possible to run the command with other paths and copy the resulting folders into the project afterwars. For that, the paths below can be changed accordingly.

    It is also possible to change the initial behaviour of the pipeline if the normalization-step is required or either milvus or csvs should not be used.
    See the documentation of the flags below for more information.

    Note that if saving of the embeddings in csvs or milvus is deactivated, the flags for inference- and add_new_embeddings-pipelines need to be updated accordingly.
    """

    temp_base_dir = Path(__file__).resolve().parent
    base_dataset_path = temp_base_dir / "app" / "media" / "BaseImages"
    region_dataset_path = temp_base_dir / "app" / "media" / "RegionImages"
    csv_folder_path = temp_base_dir / "app" / "media" / "csv"

    # delete milvus collection if one exists
    drop_collection(milvus_collection_name)

    # Call the pipeline with paths
    initial_pipeline.run_initial_data_pipeline(
        base_dataset_path,  # path to base images (mandatory)
        region_dataset_path,  # path to region images (mandatory)
        csv_folder_path,  # path to csv-folder (mandatory)
        model=_default_cnn_model_,  # uses the default cnn model for embedding calculation
        normalize=False,  # flag whether or not images should be normalized. False if RegionImages already exist. Set true if only BaseImages exist.
        save_images=False,  # flag whether or not normalized images should be saved. False if RegionImages already exist. Set true if only BaseImages exist.
        save_csvs=True,  # flag whether or not to save calculated embeddings in csv-files. True per default for data redundancy
        save_milvus=True,  # flag whether or not to save calculated embeddings in milvus vector database. requires running database containers (docker).
        milvus_collection_name=milvus_collection_name,  # default milvus collection name
        model_name=default_model_name,  # default model name, HAS to correspond with model
    )


@cli.command("bulk_import_calculations")
def bulk_import_with_initial_data_pipeline():
    """
    Run the initial data pipeline for bulk-imports of images and corresponding data into already existing structure.

    This function as is assumes that the structure described in `setup_new_project_with_initial_data_pipeline` was already created, filled, and should now be extended by adding a bunch of new images at once.


    Prerequisites:
        - original images that should be added lie in a temporary folder like NewImages (*path can be updated according to your needs, do **NOT** use BaseImages folder with already existing data*)
        - TempRegionImages folder has been created to hold NewImages' normalized images (*path can be updated according to your needs, do **NOT** use RegionImages unless you plan on re-calculating the embeddings for the whole dataset from scratch. For that case, embeddings.csvs and milvus-database need to be deleted manually beforehand to not duplicate existing data*)
        - csv-folder is the same as in initial run of the pipeline to add the calculated embeddings correctly to the embeddings.csvs per region
        - have the metadata (at least uuid, age, gender) for the new images available. (*Use format of Metadata.csv to format it correctly in a separate csv-file, so it is easier to copy later.*)

    Walkthrough:
        - first, pipeline creates normaized images from NewImages in TempRegionImages
        - then, pipeline calculates embeddings and saves them in embeddings.csvs per region in csv-folder
        - when pipeline is done, you
            - copy every image from NewImages that has correctly been handled by the pipeline into BaseImages. It is now part of your new BaseDataset.
            - copy the corresponding region-images (with the same uuids as the NewImages) from TempRegionImages into RegionImages.
            - copy corresponding metadata (same uuids) into Metadata.csv in csv-folder. Keep the correct format in mind.

    By changing the flags, it is also possible to use already normalized region-images or recalculate embeddings from scratch. For further information on the use of the flags see `setup_new_project_with_initial_data_pipeline` or docstring of `run_initial_data_pipeline`.
    """

    temp_base_dir = Path(__file__).resolve().parent
    base_dataset_path = temp_base_dir / "app" / "media" / "NewImages"
    region_dataset_path = temp_base_dir / "app" / "media" / "TempRegionImages"
    csv_folder_path = temp_base_dir / "app" / "media" / "csv"

    # Call the pipeline with paths
    initial_pipeline.run_initial_data_pipeline(
        base_dataset_path,
        region_dataset_path,
        csv_folder_path,
        normalize=True,
        save_images=True,
        save_csvs=True,
        save_milvus=True,
    )


@cli.command("initial_dataset_filter")
def filter_11k_dataset():
    """Run filter_11k function to filter usable images from the 11K dataset.
    See filter_11k_hands-docstring for further information.

    Ideally build via os.path or pathlib.Path, for example see function setup_new_project_data.
    Do NOT use paths to default project folders in this function.
    """
    # TODO: Set correct paths before running the pipeline
    folder_path_initial_dataset = "path/to/image/folder"  # current dataset
    initial_csv_path = "path/to/csv"  # e.g. "path\to\HandInfo.csv"
    filtered_dataset_path = ""  # e.g. "NewDataset" or "BaseDataset"
    new_csv_path = "CSV_filtered.csv"  # absolute path to new metadata-csv
    filter_11k_hands(folder_path_initial_dataset, initial_csv_path, filtered_dataset_path, new_csv_path)


@cli.command("setup_csv_logging")
def initial_setup_csv_logging():
    """Run the setup csv-logging funktion manually to create logs-folder and log-csvs for backend."""
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
        with zipfile.ZipFile(backup_zip_path, "w", zipfile.ZIP_DEFLATED) as backup_zip:
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
        with zipfile.ZipFile(backup_path, "r") as backup_zip:
            backup_zip.extractall(Path("."))  # Restore to current directory

        typer.echo("Backup successfully restored!")

    except Exception as e:
        typer.echo(f"Error restoring backup: {e}", err=True)
        typer.Exit(1)


if __name__ == "__main__":
    cli()
