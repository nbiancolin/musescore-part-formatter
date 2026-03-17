import pytest

from musescore_part_formatter.canonical.models import Measure

@pytest.fixture(scope="function")
def sample_score():
    expected_measure_data = [
        Measure(number=(i +1), is_rehearsal_mark=False, double_bar_position=None, has_notes=True, is_mm_rest_start=False, mm_rest_len=None)
        for i in range(32)
    ]
    return expected_measure_data


@pytest.fixture(scope="function")
def sample_score_with_barlines(sample_score):
    #Direct Translation of tests\test-data\sample-mscx\Test_Regular_Line_Breaks.mscx
    sample_score[15].double_bar_position = 'r'
    sample_score[16].double_bar_position = 'l'
    return sample_score


@pytest.fixture(scope="function")
def sample_score_with_rehearsal_marks(sample_score):
    sample_score[16].is_rehearsal_mark = True
    return sample_score


@pytest.fixture(scope="function")
def sample_score_with_barlines_and_rehearsal_marks(sample_score):
    sample_score[15].double_bar_position = 'r'
    sample_score[16].double_bar_position = 'l'
    sample_score[16].is_rehearsal_mark = True
    return sample_score


@pytest.fixture(scope="function")
def sample_score_mm_rests_barlines():
    expected_measure_data = [
        Measure(1, is_rehearsal_mark=False, double_bar_position=None, has_notes=False, is_mm_rest_start=True, mm_rest_len=8),
        Measure(9, is_rehearsal_mark=False, double_bar_position=None, has_notes=False, is_mm_rest_start=True, mm_rest_len=8),
    ]
    expected_measure_data[8]
    #TODO: Didn't account for MM rest with double ba and rehearsal mark.
    # DOuble bar would have to be both
    # rehearsal mark just means the start not the end