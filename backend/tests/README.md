# Tests

## Table of contents

- [Tests](#tests)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Create Tests](#create-tests)
  - [Run Tests](#run-tests)
    - [via Plugin](#via-plugin)
    - [via Console](#via-console)
  - [Test-Scenarios](#test-scenarios)
    - [Embeddings-Scenario](#embeddings-scenario)
      - [Entry point embeddings scenario](#entry-point-embeddings-scenario)
      - [Steps of Embeddings-Scenario](#steps-of-embeddings-scenario)
      - [Criteria for the selection of images](#criteria-for-the-selection-of-images)
    - [Classifier-Scenario](#classifier-scenario)
      - [Entry point classifier scenario](#entry-point-classifier-scenario)
    - [Random_Forest-Scenario](#random_forest-scenario)
      - [Entry point random forest scenario](#entry-point-random-forest-scenario)
      - [Analysis and Interpretation of results](#analysis-and-interpretation-of-results)

## Overview

The tests were implemented using pytest.

All correctly named tests in the test module run via ci-pipeline in github on PR creation or merge into main.

## Create Tests

- Pytest recognizes test-files with "tests\_" at the beginning of the name, e.g. "tests_name_of_the_module_to_test".
- The test-functions need to start with "test\_" as well.
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

The test scenarios in the `tests/scenarios`-folder are used to generate data for the analysis and optimisation of individual components of the application, such as embeddings, distance calculation or classification.

They are typically triggered via pytest and the function to use them can be found commented out at the start of the respective script. It should be commented out again after use to avoid running the test-scenario with the ci-pipeline.

### Embeddings-Scenario

Scenario for the different models for calculating the embeddings. Models that are available: Densenet_121, Densenet_169, Resenet_50
The aim is to generate data for subsequent analysis of which model is most suitable. For the evaluation, the duration for the calculation of all embeddings is measured. In addition, the distance/similarity between an image of a person and the other images of the same person in the data set is determined.

Images of the same person should provide the most similar embeddings compared to other people despite different hand positions or sides. Also the same picture should have a distance of 0/ similarity of 1

**Default settings:**

distance (csv)/ similarity (milvus) calculation with cosine
k = 10

#### Entry point embeddings scenario

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
- embeddings calculation with each model
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

Scenario to test and evaluate implemented classifiers by classifying all images from the BaseImages-folder and saving the results. Saves results of region-classifiers as well as ensemble classifiers.

#### Entry point classifier scenario

Use the scenario by running the test-function `test_scenario_classifier` via pytest.
Read the prerequisites-comment above the function in `classifier_scenario.py` for further instructions on what to prepare and how to run the scenario.

Results of region classifications with labels can be used for random_forest_feature_importance_scenario.
Results of ensemble classifications can be used for evaluation of overall performance and hyperparameter-tests (e.g. weights, k).

**Default settings:**

- uses prod data (all images from BaseImages and its metadata)
- uses csv-embeddings and distance calculation (use of milvus not implemented because they are nearly interchangeable)
- k = 5
- filters same image from nearest neighbours before classification to not scew results

Be sure to isolate results from different test runs by moving or renaming the result csvs. If in doubt, check the number of entries in csvs against the number of base images.

### Random_Forest-Scenario

Scenario to calculate feature importances for the classifiers via RandomForest and linear models.

Uses the classification results per region as well as the correct labels to first train the RandomForest and linear models and then determine likely feature importances in form of built-in importances, permutation importances as well as the coefficients of the linear models.

Those feature importances are then used to determine possible weights for the ensemble classifiers.
To test those weights, please see [Classifier-Scenario](#classifier-scenario).

#### Entry point random forest scenario

Run the scenario by running the test-function `test_calculate_feature_importances` via pytest.
Read the prerequisites-comment above the function in `random_forest_feature_importance_scenario.py` for further instructions on what to prepare and how to run the scenario.

_From the prerequisites_:
_For this scenario, you'll need the classification data for age and gender in form of csv-files. They are created by running the classifier_scenario beforehand. The data from the ensemble-classification is not needed here._

#### Analysis and Interpretation of results

The results are printed to the console.

**RandomForestRegressor**
The first importances will be for the age-classifier. A RandomForestRegressor is used here since age is not categorized in classes.
Since a random_search is used to determine the best possible parameters, those found and used are printed first. It is possible that these differ from run to run. If there is a specific set of parameters you want to use per default, skip the random search and initialize the RandomForest accordingly.

The Importances printed here are

- Gini Importance (built-in feature-importances of the RandomForest)
- Permutation Importance (seen as improved/ more stable model to calculate importances)

The hand-regions are then ranked by feature importance, the most important Features rise to the top.

**RandomForestClassifier**
The second set of importances are calculates for the gender-classification. A RandomForestClasifier is used since out gender-classifier has only two classes.
The feature importances and printing order are the same as for the RandomForestRegressor.

**Linear models**
As third option, linear models are trained. LinearRegression is used for age-classification and LogisticRegression for gender-classification.
After the models are trained, their coefficients (so, their weights) are printed.
They are not labeled, but they are ordered in the same way as the region columns in the classification-csvs, so in order of the hand-regions. That way, they can be associated with the correct region and interpreted.

**Result**
Since the RandomForest-Importances were more similar to one another than the linear models' and easier to interpret, we prioritized the RandomForest-Importances. The weights currently in use for the ensemble classifiers (specifically for age, since for gender, the weights did not make much of a difference) were used by manually creating different sets of weights that loosely correspond to the percieved feature importances. For a first step, we chose increments of 0.25 to map importances to weights, with 1 as the highest possible weight (highest importances) and 0.25 as the lowest.

The weights currently in use were the ones producing the best outcome (which we defined as the most correctly guessed genders/ the least deviation from the correct ages).
