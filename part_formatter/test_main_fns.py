import pytest
import warnings

from part_formatter import format_mscz, FormattingParams


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