# Tests

- [Tests](#tests)
  - [Create Tests](#create-tests)
  - [Run Tests](#run-tests)
    - [via Plugin](#via-plugin)
    - [via Console](#via-console)
  - [Test-Scenarios](#test-scenarios)
    - [Embeddings-Scenario](#embeddings-scenario)
    - [Classifier-Scenario](#classifier-scenario)
    - [Random\_Forest-Scenario](#random_forest-scenario)

The tests were implemented using pytest.

All correctly named tests in the test module run via ci-pipeline in github on PR creation or merge into main.

## Create Tests

- Pytest recognizes test-files with *tests_* at the beginning of the name, e.g. *tests_name_of_the_module_to_test*.
- The test-functions need to start with *test_* as well.
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

### Embeddings-Scenario

tbd

### Classifier-Scenario

tbd

### Random_Forest-Scenario

tbd
