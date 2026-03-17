from typing import TypedDict, Any, Literal

from dataclasses import dataclass


@dataclass
class FormattingConfig:
    num_measures_per_line: int

    balance_mode: Literal["simple", "three-line"]

    #balance flags
    balance_mm_rest_line_breaks: bool = True


class TitleBoxProperties(TypedDict):
    # For these values, to set a field blank, pass in "" (empty string)
    # To leave them as is, pass in None
    title: str | None
    subtitle: str | None
    composer: str | None
    lyricist: str | None
    part_name: str | None


class Defaults:

    # DEFAULTS:
    NUM_MEASURES_PER_LINE = 6



