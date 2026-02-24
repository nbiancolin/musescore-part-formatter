from typing import TypedDict, Any


class FormattingConfig(TypedDict):
    num_measures_per_line: int


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



