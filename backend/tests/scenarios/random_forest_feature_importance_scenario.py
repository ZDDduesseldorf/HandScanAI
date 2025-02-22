import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression, LinearRegression

from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import HandRegions


"""
Prerequisites:
For this scenario, you'll need the classification data for age and gender in form of csv-files (see file-paths below).
They are created by running the classifier_scenario beforehand. The data from the ensemble-classification is not needed here.

To run this scenario, comment in the function test_calculate_feature_importances below
and run it on the console from the /backend-folder via 'pytest -s tests/scenarios/random_forest_feature_importance_scenario.py'.
The -s flag is needed to get the console output.

The results are printed to the console and you can copy them from there to analyze them.
"""
# TODO: comment in to run the feature importance calculation
"""def test_calculate_feature_importances():
    temp_base_dir = Path(__file__).resolve().parent
    path_to_age_csv = temp_base_dir / "result_csvs" / "classifier" / "classification_data_age.csv"
    path_to_gender_csv = temp_base_dir / "result_csvs" / "classifier" / "classification_data_gender.csv"

    calculate_feature_importances(path_to_age_csv, path_to_gender_csv)"""


def calculate_feature_importances(path_to_age_csv: Path, path_to_gender_csv: Path):
    """
    Calculates the feature importances for both the RandomforestClassifier (gender) and RandomForestRegressor (age) and prints them.

    Calculated feature importances are Gini Importance, Permutation Importance and coefficients of linear regression models.

    Args:
        path_to_age_csv (Path): absolute path to csv with classification data from age region classifiers
        path_to_gender_csv (Path): absolute path to csv with classification data from gender region classifiers
    """
    print()
    print("---AGE---")
    X_age, y_age = load_random_forest_data(path_to_age_csv)  # noqa: N806
    X_age_train, X_age_test, y_age_train, y_age_test = prepare_data_for_random_forest(X_age, y_age)  # noqa: N806
    forest_age = random_forest_regressor(X_age_train, y_age_train)
    calculate_feature_importance(forest_age, X_age_test, y_age_test)

    print()
    print("---GENDER---")
    X_gender, y_gender = load_random_forest_data(path_to_gender_csv)  # noqa: N806
    X_gender_train, X_gender_test, y_gender_train, y_gender_test = prepare_data_for_random_forest(X_gender, y_gender)  # noqa: N806
    forest_gender = random_forest_classifier(X_gender_train, y_gender_train)
    calculate_feature_importance(forest_gender, X_gender_test, y_gender_test)

    print()
    print("Linear Models")
    create_linear_models(X_age_train, y_age_train, X_gender_train, y_gender_train)


def load_random_forest_data(path_to_csv: Path):
    """
    Loads data from csv into Dataframe and does data and label split.

    Args:
        path_to_csv (Path): absolute path to csv with classification data

    Returns:
        (X, y) (pd.DataFrame, pd.DataFrame):
        - X: data containing classification results per region
        - y: label (age or gender)
    """
    data_raw = pd.read_csv(path_to_csv)

    data = data_raw.drop(Keys.UUID.value, axis=1)

    y = data["label"]
    X = data.drop("label", axis=1)  # noqa: N806

    return X, y


def prepare_data_for_random_forest(X: pd.DataFrame, y: pd.DataFrame):  # noqa: N803
    """
    Does train and test split 80:20.

    Args:
        X (pd.DataFrame): dataframe holding the data
        y (pd.DataFrame): dataframe holding the corresponding labels

    Returns:
        (X_train, X_test, y_train, y_test) (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame): train-test-split data and label
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)  # noqa: N806
    return X_train, X_test, y_train, y_test


def random_forest_regressor(X_train: pd.DataFrame, y_train: pd.DataFrame) -> RandomForestRegressor:  # noqa: N803
    """
    Creates a random forest regressor via hyperparameter search used for calculating feature importance for age prediction.

    Args:
        X_train (pd.DataFrame): training data from the train-test-split
        y_train (pd.DataFrame): corresponding labels

    Returns:
        forest (RandomForestRegressor): best RandomForestRegressor for the given training data
    """

    forest = RandomForestRegressor()
    parameters = {
        "max_depth": [1, 2, 3, 6, 8, 10],
        "min_samples_leaf": [1, 3, 5, 8, 9, 12],
        "n_estimators": [10, 20, 30, 50, 80, 100],
    }
    random_search = RandomizedSearchCV(forest, parameters, n_iter=20, verbose=2, random_state=0)
    random_search.fit(X_train, y_train)
    print(f"RandomForestRegressor best params random_search: {random_search.best_params_}")
    return random_search.best_estimator_


def random_forest_classifier(X_train: pd.DataFrame, y_train: pd.DataFrame) -> RandomForestClassifier:  # noqa: N803
    """
    Creates a random forest classifier via hyperparameter search used for calculating feature importance for gender prediction.

    Args:
        X_train (pd.DataFrame): training data from the train-test-split
        y_train (pd.DataFrame): corresponding labels

    Returns:
        forest (RandomForestRegressor): best RandomForestClassifier for the given training data
    """

    forest = RandomForestClassifier()
    parameters = {
        "max_depth": [1, 2, 3, 6, 8, 10],
        "min_samples_leaf": [1, 3, 5, 8, 9, 12],
        "n_estimators": [10, 20, 30, 50, 80, 100],
    }
    random_search = RandomizedSearchCV(forest, parameters, n_iter=20, verbose=2, random_state=0)
    random_search.fit(X_train, y_train)
    print(f"RandomForestClassifier best params random_search: {random_search.best_params_}")
    return random_search.best_estimator_


def calculate_feature_importance(
    forest: (RandomForestClassifier | RandomForestRegressor),
    X_test: pd.DataFrame,  # noqa: N803
    y_test: pd.DataFrame,
):
    """
    Calculates the feature importances for either a RandomforestClassifier (gender) or RandomForestRegressor (age) via built-in importance and permutation-importance and prints them.

    Args:
        forest (RandomForestClassifier | RandomForestRegressor): RandomforestClassifier for gender or RandomForestRegressor for age classification
        X_test (pd.DataFrame): test data from the train-test-split
        y_test (pd.DataFrame): corresponding labels
    """
    feature_names = [
        HandRegions.HAND_0.value,
        HandRegions.HANDBODY_1.value,
        HandRegions.THUMB_2.value,
        HandRegions.INDEXFINGER_3.value,
        HandRegions.MIDDLEFINGER_4.value,
        HandRegions.RINGFINGER_5.value,
        HandRegions.LITTLEFINGER_6.value,
    ]
    # Built-in feature importance (Gini Importance)
    importances = forest.feature_importances_
    feature_imp_df = pd.DataFrame({"Feature": feature_names, "Gini Importance": importances}).sort_values(
        "Gini Importance", ascending=False
    )
    print(feature_imp_df)

    result = permutation_importance(forest, X_test, y_test, n_repeats=10, random_state=0, n_jobs=-1)
    perm_imp_df = pd.DataFrame(
        {"Feature": feature_names, "Permutation Importance": result.importances_mean}
    ).sort_values("Permutation Importance", ascending=False)
    print(perm_imp_df)


def create_linear_models(
    X_age_train: pd.DataFrame,  # noqa: N803
    y_age_train: pd.DataFrame,
    X_gender_train: pd.DataFrame,  # noqa: N803
    y_gender_train: pd.DataFrame,
):
    """
    Creates two linear models for the age- and gender-classification and prints their coefficients. Can be interpreted or used as weights.
    Results were not prioritized as high as the RandomForest-Importances.

    Args:
        X_age_train (pd.DataFrame): training data from the train-test-split für age classification
        y_age_train (pd.DataFrame): corresponding labels
        X_gender_train (pd.DataFrame): training data from the train-test-split für gender classification
        y_gender_train (pd.DataFrame): corresponding labels
    """
    linear_model = LinearRegression()
    linear_model.fit(X_age_train, y_age_train)
    print(f"linear model coefs (age): \n{linear_model.coef_}")

    logistic_model = LogisticRegression()
    logistic_model.fit(X_gender_train, y_gender_train)
    print(f"logistic model coefs (gender): \n{logistic_model.coef_}")
