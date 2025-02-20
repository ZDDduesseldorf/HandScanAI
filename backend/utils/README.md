# Utils

- [Utils](#utils)
  - [csv-utils](#csv-utils)
  - [image-utils](#image-utils)
  - [key-enums](#key-enums)
  - [logging-utils](#logging-utils)
  - [uuid-utils](#uuid-utils)

## csv-utils

The csv-utils module contains

- functions to check for the existence of folders and files
- functions to save information to csv-files (e.g. as alternative to databases or logging information)

## image-utils

The image-utils module contains

- functions to construct an image path
- function to copy images from one folder to another
- functions to load an image via opencv

## key-enums

The key-enums module contains the following Enums:

- **HandRegions**: Enum that is used as keys to standardize region-dictionaries across different modules of the backend (e.g. hand-normalization, pipelines)
- **PipelineAPIKeys**: Enum that is used as keys for dictionaries and dataframes directly related to the API
- **PipelineDictKeys**: Enum that is used as keys for dictionaries and dataframes used in different steps in the backend-pipelines (see pipelines-module)

## logging-utils

The logging-utils module contains functions to log information for later evaluation in csv-files:

- **nearest_neighbours**: saves information about the current query-image and its nearest neighbours (function `logging_nearest_neighbours`)
- **classification**: saves information about the current query-image, it's classification results, ranges and confidence of the model (function `logging_classification`)
- **input_data**: saves information about the actual metadata of the current query-image after the user input (function `logging_input_data`)

See file and docstrings for further information.

## uuid-utils

The uuid-utils module contains the function to generate a uuid (used for image-names and subsequently used as key/ID).
