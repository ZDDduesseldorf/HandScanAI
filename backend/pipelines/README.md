# Pipelines

TODO: Add information on pipelines

## Initial Data Pipeline

This pipeline (`initial_data_pipeline.py`) is used to provide the initial chunk of data for the databases when they are built from the ground up OR is used when a whole new dataset is added to existing databases. Initially, it is used to filter and process relevant images from the 11k dataset.

The following diagrams show the concept of the pipeline as of 10.12.24 with temporary saving images and metadata locally.
TODO: Update when databases get introduced.
![A diagram showing the pipeline steps validation (which yields metadata and a base dataset of images), hand-normalization (which yields a region dataset), calculation of embeddings and the creation and extension of search trees (which yield updated search trees).](readme_data/initial_data_pipeline_concept_rough_1.png)
![A diagram showing the pipeline's more detailed steps and their results.](readme_data/initial_data_pipeline_concept_medium_detail_1.png)

TODO: Add dataflow and data types of pipeline

### Use the initial data pipeline

Before using the pipeline, make sure all the necessary paths for loading and saving the images and other data are updated/ correct (tbd better documentation of what that all is).

Then, the pipeline can be run from the `/backend`-folder via console:
`python manage.py initial_data_pipeline`. (Windows. For other ways to use `manage.py` by running python from the console, see `README` under `/backend`).

## Inference Pipeline

## Add new Embeddings Pipeline
