import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance

from utils.key_enums import PipelineDictKeys as Keys
from utils.key_enums import HandRegions


def load_random_forest_data(path_to_csv):
    data_raw = pd.read_csv(path_to_csv)

    data = data_raw.drop(Keys.UUID.value, axis=1)

    y = data["label"]
    X = data.drop("label", axis=1)  # noqa: N806

    return X, y


def prepare_data_for_random_forest(X, y):  # noqa: N803
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)  # noqa: N806
    return X_train, X_test, y_train, y_test


def random_forest_regressor(X_train, y_train):  # noqa: N803
    forest = RandomForestRegressor(n_estimators=50, random_state=0, max_depth=4)
    forest.fit(X_train, y_train)
    return forest


def random_forest_classifier(X_train, y_train):  # noqa: N803
    forest = RandomForestClassifier(n_estimators=50, random_state=0, max_depth=4)
    forest.fit(X_train, y_train)
    return forest


def feature_importance_age(forest_age, X_test, y_test):  # noqa: N803
    result = permutation_importance(forest_age, X_test, y_test, n_repeats=10, random_state=0, n_jobs=-1)
    feature_names = [
        HandRegions.HAND_0.value,
        HandRegions.HANDBODY_1.value,
        HandRegions.THUMB_2.value,
        HandRegions.INDEXFINGER_3.value,
        HandRegions.MIDDLEFINGER_4.value,
        HandRegions.RINGFINGER_5.value,
        HandRegions.LITTLEFINGER_6.value,
    ]
    perm_imp_df = pd.DataFrame(
        {"Feature": feature_names, "Permutation Importance": result.importances_mean}
    ).sort_values("Permutation Importance", ascending=False)
    print(perm_imp_df)

    # Built-in feature importance (Gini Importance)
    importances = forest_age.feature_importances_
    feature_imp_df = pd.DataFrame({"Feature": feature_names, "Gini Importance": importances}).sort_values(
        "Gini Importance", ascending=False
    )
    print(feature_imp_df)


def calculate_feature_importances(path_to_age_csv, path_to_gender_csv):
    print("---AGE---")
    X_age, y_age = load_random_forest_data(path_to_age_csv)  # noqa: N806
    X_age_train, X_age_test, y_age_train, y_age_test = prepare_data_for_random_forest(X_age, y_age)  # noqa: N806
    forest_age = random_forest_regressor(X_age_train, y_age_train)
    feature_importance_age(forest_age, X_age_test, y_age_test)
    print("---GENDER---")
    X_gender, y_gender = load_random_forest_data(path_to_gender_csv)  # noqa: N806
    X_gender_train, X_gender_test, y_gender_train, y_gender_test = prepare_data_for_random_forest(X_gender, y_gender)  # noqa: N806
    forest_gender = random_forest_classifier(X_gender_train, y_gender_train)
    feature_importance_age(forest_gender, X_gender_test, y_gender_test)
