from classifier.weighted_classification import weighted_classifier
from utils.key_enums import HandRegions
from utils.key_enums import PipelineDictKeys as DictKeys
from utils.key_enums import PipelineAPIKeys as APIKeys
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal


@pytest.fixture()
def dict_all_info_knn():
    yield {
        HandRegions.HAND_0.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
        HandRegions.HANDBODY_1.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
        HandRegions.THUMB_2.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
        HandRegions.INDEXFINGER_3.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
        HandRegions.MIDDLEFINGER_4.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
        HandRegions.RINGFINGER_5.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
        HandRegions.LITTLEFINGER_6.value: pd.DataFrame(
            {
                DictKeys.UUID.value: ["1", "2"],
                DictKeys.DISTANCE.value: [0, 0.5],
                DictKeys.AGE.value: [20, 26],
                DictKeys.GENDER.value: [0, 1],
            },
        ),
    }


def test_weighted_classifier(dict_all_info_knn):
    ensemble_df = pd.DataFrame(
        [
            {
                APIKeys.CLASSIFIED_AGE.value: 22.0,
                APIKeys.MIN_AGE.value: 20.0,
                APIKeys.MAX_AGE.value: 26.0,
                APIKeys.CONFIDENCE_AGE.value: 0,
                APIKeys.CLASSIFIED_GENDER.value: 0,
                APIKeys.CONFIDENCE_GENDER.value: 2 / 3,
            }
        ]
    )
    result_df, _, _ = weighted_classifier(dict_all_info_knn)

    assert_frame_equal(ensemble_df, result_df)
