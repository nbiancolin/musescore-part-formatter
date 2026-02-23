import pytest
import xml.etree.ElementTree as ET

from musescore_part_formatter.canonical.convert import convert_staff_to_canonical_part
from musescore_part_formatter.canonical.models import Measure

SAMPLE_MSCX_PATH = "tests\\test-data\\sample-mscx\\Test_Regular_Line_Breaks.mscx"
SAMPLE_MSCX_WITH_MM_REST_PATH = "tests\\test-data\\sample-mscx-new\\sample-mscx-new.mscx"


def generate_sample_mscx_measure_data():
    expected_measure_data = [
        Measure(number=(i +1), is_rehearsal_mark=False, double_bar_position=None, has_notes=True, is_mm_rest_start=False, mm_rest_len=None)
        for i in range(32)
    ]
    expected_measure_data[15].double_bar_position = 'r'
    expected_measure_data[16].double_bar_position = 'l'
    return expected_measure_data

def generate_sample_mscx_mm_rest_data():
    
    """"
    Weitd behaviour with MM rests
    
    the SECOND measure of the MM rest has the "MM Rest" attribute I think.....
    Maybe create a new test to confirm
    
    """
    expected_measure_data = [
        Measure(number=(i +1), is_rehearsal_mark=False, double_bar_position=None, has_notes=True, is_mm_rest_start=False, mm_rest_len=None)
        for i in range(8)
    ] + [
        Measure(number=9, is_rehearsal_mark=False, double_bar_position=None, has_notes=False, is_mm_rest_start=True, mm_rest_len=4)
    ] + [
        Measure(number=(12 + i +1), is_rehearsal_mark=False, double_bar_position=None, has_notes=True, is_mm_rest_start=False, mm_rest_len=None)
        for i in range(4)
    ] + [
        Measure(number=17, is_rehearsal_mark=False, double_bar_position=None, has_notes=False, is_mm_rest_start=True, mm_rest_len=8)
    ] + [
        Measure(number=(24 + i +1), is_rehearsal_mark=False, double_bar_position=None, has_notes=True, is_mm_rest_start=False, mm_rest_len=None)
        for i in range(8)
    ]
    expected_measure_data[12].double_bar_position = 'r'
    expected_measure_data[13].double_bar_position = 'l'
    return expected_measure_data

@pytest.mark.parametrize(
    "mscx_path, generate_measure_data", [(SAMPLE_MSCX_PATH, generate_sample_mscx_measure_data), (SAMPLE_MSCX_WITH_MM_REST_PATH, generate_sample_mscx_mm_rest_data)]
)
def test_convert_sample_score_to_canonical(mscx_path, generate_measure_data):

    parser = ET.XMLParser()
    tree = ET.parse(mscx_path, parser)
    root = tree.getroot()
    score = root.find("Score")
    if score is None:
        raise ValueError("No <Score> tag found in the XML.")

    staves = score.findall("Staff")
    staff = staves[0]  # noqa  -- only add layout breaks to the first staff
    
    part = convert_staff_to_canonical_part(staff)
    sample_mscx_measure_data = generate_measure_data()

    assert len(part.measures) == len(sample_mscx_measure_data)

    i = 0
    for m1, m2 in zip(part.measures, sample_mscx_measure_data):
        assert m1 == m2, f"Index {i}: Detected:\n{m1}\nVerification:\n{m2}"
        i += 1
