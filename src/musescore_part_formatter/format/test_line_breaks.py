import pytest


from musescore_part_formatter.format.config import FormattingConfig
from musescore_part_formatter.format.line_breaks import add_line_breaks

from musescore_part_formatter.canonical.models import Part


@pytest.fixture(scope="function")
def sample_config():
    return FormattingConfig(num_measures_per_line=6)


@pytest.mark.parametrize(
    "nmpl, expected_line_break_indices",
    [(4, [3, 7, 11, 15, 19, 23, 27]), (6, [5, 11, 17, 23, 29])],
)
def test_line_break_placement_on_regular_score(
    sample_score, nmpl, expected_line_break_indices
):

    part = Part("idk", measures=sample_score)
    config = FormattingConfig(num_measures_per_line=nmpl)
    # WHEN
    formatted_part = add_line_breaks(part, config)

    # THEN
    indices_w_line_break = [
        i
        for i in range(len(formatted_part.measures))
        if formatted_part.measures[i].add_line_break
    ]

    assert expected_line_break_indices == indices_w_line_break


@pytest.mark.parametrize(
    "nmpl, expected_line_break_indices",
    [(4, [3, 7, 11, 15, 19, 23, 27]), (6, [5, 11, 15, 21, 27])],
)
def test_line_break_placement_on_score_with_barlines(
    sample_score_with_barlines, nmpl, expected_line_break_indices
):

    part = Part("idk", measures=sample_score_with_barlines)
    config = FormattingConfig(num_measures_per_line=nmpl)
    # WHEN
    formatted_part = add_line_breaks(part, config)

    # THEN
    indices_w_line_break = [
        i
        for i in range(len(formatted_part.measures))
        if formatted_part.measures[i].add_line_break
    ]

    assert expected_line_break_indices == indices_w_line_break


@pytest.mark.parametrize(
    "nmpl, expected_line_break_indices",
    [(4, [3, 7, 11, 15, 19, 23, 27]), (6, [5, 11, 15, 21, 27])],
)
def test_line_break_placement_on_score_with_rehearsal_marks(
    sample_score_with_rehearsal_marks, nmpl, expected_line_break_indices
):

    part = Part("idk", measures=sample_score_with_rehearsal_marks)
    config = FormattingConfig(num_measures_per_line=nmpl)
    # WHEN
    formatted_part = add_line_breaks(part, config)

    # THEN
    indices_w_line_break = [
        i
        for i in range(len(formatted_part.measures))
        if formatted_part.measures[i].add_line_break
    ]

    assert expected_line_break_indices == indices_w_line_break


@pytest.mark.parametrize(
    "nmpl, expected_line_break_indices",
    [(4, [3, 7, 11, 15, 19, 23, 27]), (6, [5, 11, 15, 21, 27])],
)
def test_line_break_placement_on_score_with_barlines_and_rehearsal_marks(
    sample_score_with_barlines_and_rehearsal_marks, nmpl, expected_line_break_indices
):

    part = Part("idk", measures=sample_score_with_barlines_and_rehearsal_marks)
    config = FormattingConfig(num_measures_per_line=nmpl)
    # WHEN
    formatted_part = add_line_breaks(part, config)

    # THEN
    indices_w_line_break = [
        i
        for i in range(len(formatted_part.measures))
        if formatted_part.measures[i].add_line_break
    ]

    assert expected_line_break_indices == indices_w_line_break


def test_line_break_placement_mm_rest_balancing():
    pass