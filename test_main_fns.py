import pytest
import warnings
import tempfile
import shutil
import xml.etree.ElementTree as ET
import os

from part_formatter import format_mscz, format_mscx, FormattingParams
from part_formatter.utils import _measure_has_line_break


@pytest.mark.parametrize("style", ("jazz", "broadway"))
def test_mscz_formatter_works(style):
    input_path = "tests/test-data/New-Test-Score.mscz"
    output_path = f"tests/test-data/New-Test-Score-{style}-processed.mscz"

    params: FormattingParams = {
        "selected_style": style,
        "show_number": "1",
        "show_title": "My Show",
        "num_measures_per_line_part": 6,
        "num_measures_per_line_score": 4
    }

    res = format_mscz(input_path, output_path, params)
    assert res
    warnings.warn("Inspect processed files and confirm they look good! :sunglasses: ")


def test_params_incorrect():
    pass
#TODO: Quickly test what jappens if you pass in bogus params and ensure that its caught

@pytest.mark.parametrize("barlines, nmpl", [
    (True, 4),
    # (True, 6),
    # (False, 4),
    # (False, 6),
])
def test_regular_line_breaks(barlines, nmpl):
    #eg, 32 bar file with notes, barline at bar 16.
    # set num measures per line to be 4
    # assert that the XML is formatted correctly
    # use format mscx

    filename = "Test_Regular_Line_Breaks.mscx"
    params: FormattingParams = {
        "num_measures_per_line_part": nmpl,
        "num_measures_per_line_score": nmpl,
        "selected_style": "broadway",
        "show_title": "My Show",
        "show_number": "1",
    }

    if barlines:
        original_mscx_path = f"tests/test-data/sample-mscx/{filename}"
    else:
        original_mscx_path = f"tests/test-data/sample-mscx/{filename}"

    with tempfile.TemporaryDirectory() as workdir:

        #process mscx
        shutil.copy(original_mscx_path, workdir)
        temp_mscx = os.path.join(workdir, filename)
        format_mscx(temp_mscx, params)

        #check that output matches what we expect

        try:
            parser = ET.XMLParser()
            tree = ET.parse(temp_mscx, parser)
            root = tree.getroot()
            score = root.find("Score")
            if score is None:
                raise ValueError("No <Score> tag found in the XML.")


            staff = score.find("Staff")
            assert staff is not None, "I made a mistake in this test ... :/"
            measures = staff.findall("Measure")
            assert len(measures) == 32, "Something is wrong ith sample score"
            measures_with_line_breaks = [(i +1) for i in range(len(measures)) if _measure_has_line_break(measures[i])]

            for i in range((nmpl -1), 31, nmpl):
                assert _measure_has_line_break(measures[i]), f"Measure {i +1} should have had a line break, but it did not :(\n Measures with line breaks: {measures_with_line_breaks}"

            #tests for 6 fail, thats the balancing thing happening, need to figure out hwo to test for that behaviour

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            assert False