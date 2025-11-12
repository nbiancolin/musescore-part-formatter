import pytest

from musescore_part_formatter.file_inspect import (
    get_properties_from_title_box,
    get_score_properties_from_meta,
    TITLE_BOX_PROPERTIES,
)

from musescore_part_formatter.main import get_score_attributes

MUSESCORE_PATH = "tests/test-data/New-Test-Score.mscz"


def test_title_properties_retrieved_correctly():
    input_path = MUSESCORE_PATH

    res = get_score_attributes(input_path)

    EXPECTED_VALUES = {
        "title": "Test Score",
        "subtitle": "Subtitle",
        "composer": "arr. Nicholas Biancolin",
    }

    for prop, value in EXPECTED_VALUES.items():
        assert res[prop] == value


def test_meta_properties_retrieved_correctly():
    input_path = MUSESCORE_PATH

    res = get_score_attributes(input_path)

    EXPECTED_VALUES = {
        "workTitle": "Test Score",
        "subtitle": "Subtitle",
        "composer": "arr. Nicholas Biancolin",
        "arranger": None,
    }

    for prop, value in EXPECTED_VALUES.items():
        assert res[f"meta_{prop}"] == value


def test_num_instruments_retrieved_correctly():
    input_path = MUSESCORE_PATH

    res = get_score_attributes(input_path)

    EXPECTED_VALUES = {
        "num_instruments": 5,
        "num_staves": 6,
    }

    for prop, value in EXPECTED_VALUES.items():
        assert res[prop] == value