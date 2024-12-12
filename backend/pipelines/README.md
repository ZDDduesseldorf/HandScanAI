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

This pipeline (inference_pipeline.py) is used to predict the age and gender of an image.

The following diagram shows the flow of the pipeline:
![A diagram showing the pipeline steps of validation (provides image), hand normalisation (which provides a region dataset), calculation of embeddings, search for the knn (provides k nearest neighbours) and classification (prediction of age and gender).](readme_data/inference_pipeline_concept.png)
The following diagram shows the inputs and outputs of the individual steps:
![A diagram describing the input and output data types of the pipeline shown above.](readme_data/inference_pipeline_datatypes.png)

TODO: Add knn-search and classification to diagram

### Use the inference pipeline

Make sure in the method get_image_path() is the correct path to the image_folder

The pipeline can be executed via the test_inference_pipeline.py from the `/backend` folder via the console:
pytest -s tests/pipelines/test_inference_pipeline.py

later:
Pipeline is triggered by the frontend after the ‘Analyse starten’ button has been pressed. The UUID of the image just taken must be transferred to the pipeline.

## Add new Embeddings Pipeline

This pipeline (add_new_embeddings_pipeline.py) is used after checking the metadata for age and gender to add the embeddings of a new image to the vectortrees. It also saves the images of each region.

The following diagram shows the flow of the pipeline:
![A diagram showing the pipeline steps of validation (provides image and metadata), hand normalisation (which provides a region dataset and saves images), calculation of embeddings and adding to the vector tree.](readme_data/add_new_embeddings_pipeline_concept.png)

The following diagram shows the inputs and outputs of the individual steps:
![A diagram describing the input and output data types of the pipeline shown above. First part until normalization ](readme_data/add_new_embeddings_pipeline_datatypes_1.png)
![Shows the second part of the datatyp diagram ](readme_data/add_new_embeddings_pipeline_datatypes_2.png)

TODO: Add integration of embeddings to vektortree

### Use the inference pipeline

Make sure in the method get_image_path() is the correct path to the image_folder and the 'output_folder_path_base' is correct.

The pipeline can be executed via the test_add_new_embeddings_pipeline.py from the `/backend` folder via the console:
pytest -s tests/pipelines/test_add_new_embeddings_pipeline.py

later:
After a check of the metadata (manually by a person or with a check-script), it is triggert by the fronted and the uuid is transferred.
