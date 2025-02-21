# Tests

- [Tests](#tests)
  - [Create Tests](#create-tests)
  - [Run Tests](#run-tests)
    - [via Plugin](#via-plugin)
    - [via Console](#via-console)
  - [Test-Scenarios](#test-scenarios)
    - [Embeddings-Scenario](#embeddings-scenario)
    - [Classifier-Scenario](#classifier-scenario)
    - [Random_Forest-Scenario](#random_forest-scenario)

The tests were implemented using pytest.

All correctly named tests in the test module run via ci-pipeline in github on PR creation or merge into main.

## Create Tests

- Pytest recognizes test-files with \_tests\__ at the beginning of the name, e.g. \_tests_name_of_the_module_to_test_.
- The test-functions need to start with \_test\_\_ as well.
- Make sure the file imports and file paths for the test-files are correct.

## Run Tests

### via Plugin

e.g. via <https://marketplace.visualstudio.com/items?itemName=littlefoxteam.vscode-python-test-adapter>

### via Console

- make sure to open console in `HandScanAI/backend`
- Run `python manage.py test`
- OR run `python -m pytest`.
  Using pytest-command, commandline-flags can be added, such as:
  - `-v` for verbose logging on console
  - `-s` to print `print()`-statements in code during testing (which is otherwise prevented by pytest)
  - path to specific test-file for only running those tests (relativ path after `/backend`)
  - For further possibilities for pytest-commands, see [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html).

## Test-Scenarios

The test scenarios are used to generate data for the analysis and optimisation of individual components of the application, such as embeddings, distance calculation or classification

### Embeddings-Scenario

Scenario for the differnt models for calcualting the embeddings. Models that are available: Densenet_121, Densenet_169, Resenet_50  
The aim is to generate data for subsequent analysis of which model is most suitable. The duration for the calculation of the embeddings and the distance/similarity between an image of a person and the other images of the same person in the data set are analysed.

Images of the same person should provide the most similar embeddings compared to other people despite different hand positions or sides. Also the same picture should have a distance of 0/ similarity of 1

Default settings:

distance (csv)/ similarity (milvus) calcualtion with cosine  
k = 10

#### Entrypoint

Run the scenario by using the test-function `pytest test_scenario_embeddings()`.  
Make sure to comment them in. The setup is executed with the default settings

Before:

- original images in folder: app/media/BaseImages
- region images in folder: app/media/RegionImages  
  if region images doesn't exists set normalize=True, save_images=True (for more information check docstring initial_data_pipeline)
- adapt uuids in `run_scenarios_embeddings` to your own test candiates

#### Steps of Embeddings-Scenario

optional create setup:

- folder and files for saving results of each model
- calculating embeddings with each model
  Duration of calcualting Embeddings is logged in the console

distance_pipeline:

- normalisation of search image
- calcualting & normalisation embeddings for each region
- using embeddings from csv or milvus for finding nearest neighbours  
  csv: calcualting cosine distance  
  milvus: uses search function of vectordb with cosine similarity
- saving results:  
  saves uuid, region, uuid of the nearest neighbour, similarity, age, gender in csv

#### Criteria for the selection of images

- Equal number of men and women
- Number of left and right hand of person as equal as possible in the data set
- 6 test candidates per left and right hand

### Classifier-Scenario

tbd

### Random_Forest-Scenario

tbd
