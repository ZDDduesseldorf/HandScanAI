# HandScanAI Backend

## Table of Contents

- [HandScanAI Backend](#handscanai-backend)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
    - [app](#app)
    - [classifier](#classifier)
    - [embeddings](#embeddings)
    - [hand-normalization](#hand-normalization)
    - [lib](#lib)
    - [logs](#logs)
    - [pipelines](#pipelines)
    - [tests](#tests)
    - [utils](#utils)
    - [validation](#validation)
    - [vectordb](#vectordb)
    - [Additional Modules](#additional-modules)
    - [Setup](#setup)
  - [Development](#development)
    - [Code Checks](#code-checks)
    - [Code formatting](#code-formatting)
    - [Run tests](#run-tests)
  - [Create and Restore Backups](#create-and-restore-backups)
    - [Create Backup](#create-backup)
    - [Restore Backup](#restore-backup)
  - [Usage from the frontend](#usage-from-the-frontend)
    - [1. Backend Server](#1-backend-server)
    - [2. Use The API](#2-use-the-api)

## Project Structure

An overview of the project directory structure and a brief description of the most important folders and files.

### app

The `app` directory contains the main application and the routes for the FastAPI project. Here are the most important components and their functions:

- `main.py`: The entry point of the application. This is where the FastAPI instance is created and the routes are registered.
- `routes.py`: This is where the various router modules are registered, defining the API endpoints.
- `lifetime.py`: This is where functions are defined that are executed when the application starts and stops.
- `api/`: This is where the the different router modules are implemented, such as graphql, rest and websockets. Check out the readme there for further information.
- `static/`: This is where static files, such as images, etc., are located.
- `core/`: This directory contains the configuration files of the fastapi server.
- `db/`: This directory is responsible for data storage in the backend and includes the defintion of the models and triggers.
- `media/`: This directory contains files, that are created and used dynamically by the application. The directory is created by the application, should not be in the repo.

This structure helps keep the code clean and modular, making it easier to maintain and extend the application.

### classifier

The `classifier` directory contains the modules that are used to classify the age and gender of the results of the nearest neighbours. There are weighted and unweighted classifications. See the classifier-Readme for further information.

### embeddings

The directory `embeddings` contains the modules that are used for embeddings calculation via CNNs. Those embeddings are later used to determine similarities between images. See the embeddings-Readme for further information.

### hand-normalization

The `hand-normalization` module processes hand images to prepare them for embedding calculations. It includes functions for segmenting, resizing, and saving hand region images. This ensures consistent input for further analysis and classification. See the hand-normalization-Readme for further information.

### lib

The `lib` directory contains general library customized functions and utilities that can be used in various parts of the application. These functions are often reusable and abstract complex logic to make it more accessible.

### logs

The directory `logs` is not committed to the repo but is needed to store csv-files that are used to collect various data. It gets created automatically upon starting the backend docker container or has to be set up manually. For further information, see [Setup](#setup).

### pipelines

The `pipelines` module includes various data processing pipelines that string together several functionalities of other modules  and form the main workflow of the backend. They can be used for tasks such as filtering datasets, initializing data, performing inference, and adding new embeddings and ensure efficient data handling and processing for the HandScanAI backend. Some of the pipelines are also used by the API-Endpoints. See the pipelines-Readme for further information.

### tests

The `tests` directory contains the unit and integration tests of the backend, implemented using `pytest`. Check out the tests-Readme for further instructions.

### utils

The `utils` directory contains several modules with helper functions that are useful all across the app (e.g. enums used as dict-keys or functions to save data in csv-files). See utils' Readme for further details.

### validation

The `validation` directory contains all validation components of the application, that are used in the business logic, such as validating input stream in the form of a pipeline.

### vectordb

The `vectordb` module provides a script for managing embeddings in the Milvus vector database. It includes functions for creating collections, inserting and searching embeddings, and querying or deleting records by UUID. Check out the README there for further information.

### Additional Modules

Additional modules can be added in a similar way by creating new directories and files that encapsulate specific functions and logic.

By adding new modules in this way, the codebase remains organized and modular, making it easier to maintain and extend the application.

### Setup

Setup necessary to use the application. Describes creation of folder structures and base data.

**1. setup media**
Create `backend/app/media` and inside

- `BaseImages`: contains all images of BaseDataset
- `csv`: contains Metadata.csv and {region}\_Embeddings.csv (created via `manage.py setup_new_project_data`, see `manage.py` docstrings for further information. Important: Create embedding-csvs new on every new computer/ don't copy them between devices.)
- `QueryImages`: place where images from frontend are saved
- `RegionImages`: results of hand-normalization

**2. setup logging**
The `logs-folder` in `backend` and its contents are automatically created when starting the docker container (via `startup()` in `lifetime.py`). The log-csvs lie in a folder named after the current date to make distinctions between sessions easier.

To manually set up the correct logging file structure (in case of an error or development outside of docker), in the commandline use

```sh
python manage.py setup_csv_logging
```

## Development

before you start with the development, make sure you did all the steps in the [setup](#setup)

**1. Install Docker Desktop**: Please follow the instructions and install Docker Desktop from the [Official Website](https://www.docker.com/products/docker-desktop). Also make sure docker compose is available after installation on your machine.

**2. Install Dev Container VSCode Extension**: Please install the following VSCode extension [Dev Container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). This extension makes it possible to write and edit code inside of a docker container.

**3. create .env file**: duplicate the `.env.sample` file and rename it to `.env`

**4. Development inside Container**: To develop inside the container, open the backend folder as a separate window. You will see a popup "Reopen in Container". If not, use `CTRL + SHIFT + P` and select `Dev Container: Reopen in container`. The container will be built, and VSCode will automatically configure with settings and extensions according to `devcontainer.json`.

Alternatively, you can start the project with the following command in the backend directory:

```sh
docker-compose up
```

If you wish to access the bash terminal of the container from a different terminal on your machine, please run the following command:

```sh
docker exec -it backend /bin/bash
```

**5. Access the Server**: The server is now accessible under `http://127.0.0.1:8000`.

### Code Checks

For checking code styles please run the following command:

```sh
python manage.py check
```

### Code formatting

To format the code please run the following command:

```sh
python manage.py format
```

### Run tests

To run all pytest in the application please run the following command:

```sh
python manage.py test
```

Check out the Readme in `tests`-module for further instructions on running tests.

## Create and Restore Backups

### Create Backup

To create a backup of the `volumes`, `logs`, and `app/media` folders, run the following command:

```sh
python manage.py create_backup
```

The backup will be created in the backup folder and the filename will contain the current date and time.

### Restore Backup

To restore a backup, the file must be in the `backup` folder. Then run the following command and specify the name of the backup file:

```sh
python manage.py restore_backup <backup_file>
```

**!!IMPORTANT!!**:

- All existing data will be deleted and overwritten to avoid conflicts with existing data! Also created backu
- Only create and restore backups on the same device, because calculated embeddings differ from one device to the other. So to restore one backup from one device to another, please recalculate all embeddings on the new device!

## Usage from the frontend

### 1. Backend Server

Make sure the backend server is running.

### 2. Use The API

1. **Create Scan Entry**:
   - Call the `create_scan_entry_model` mutation in GraphQL and save the returned ID.

2. **Take an Image**:
   - Use the `webcam_flow` WebSocket endpoint to take an image using the same ID.

3. **Get Scan Results**:
   - After successfully taking an image, call the `get_scan_result` query with the same ID in GraphQL to get the results of the inference pipeline.

4. **Input Real Data**:
   - To input real data of a hand, call the `update_scan_entry_model` mutation with the same ID to add the real age and real gender of the person.

5. **Confirm Entry**:
   - To confirm an entry and add its embedding to the vector database, set the `confirmed` field while updating the values in the mutation.
   - **Note**: The confirmed value can only be set to true once all necessary data is provided. Once it is set to true, you cannot edit or delete the entry anymore.
