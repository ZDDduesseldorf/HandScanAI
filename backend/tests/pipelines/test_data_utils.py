import pytest
import pandas as pd
from pipelines.data_utils import map_gender_int_to_string, map_gender_string_to_int


@pytest.fixture
def gender_int_female():
    yield 0


@pytest.fixture
def gender_int_male():
    yield 1


@pytest.fixture
def gender_str_female():
    yield "female"


@pytest.fixture
def gender_str_male():
    yield "male"


@pytest.fixture
def gender_dataframe(gender_str_female, gender_str_male):
    data = [["tom", gender_str_male], ["nick", gender_str_male], ["juli", gender_str_female]]
    # Create the pandas DataFrame
    yield pd.DataFrame(data, columns=["name", "gender"])


def test_map_gender_int_to_string(gender_int_female, gender_str_female, gender_int_male, gender_str_male):
    mapped_female = map_gender_int_to_string(gender_int_female)
    mapped_male = map_gender_int_to_string(gender_int_male)

    assert mapped_female != mapped_male
    assert mapped_female == gender_str_female
    assert mapped_male == gender_str_male


def test_map_gender_string_to_int(gender_dataframe, gender_int_female, gender_int_male):
    mapped_df = map_gender_string_to_int(gender_dataframe)

    assert mapped_df["gender"][0] == gender_int_male
    assert mapped_df["gender"][1] == gender_int_male
    assert mapped_df["gender"][2] == gender_int_female
