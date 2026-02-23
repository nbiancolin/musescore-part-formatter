from dataclasses import dataclass
from typing import Literal

@dataclass
class Measure:
    """
    Reduced Measure Class to represent what is in a measure (as far as the part formatter is concerned)
    """
    number: int
    is_rehearsal_mark: bool
    double_bar_position: Literal["l"] | Literal["r"] | None  #if None, then no double_bar

    # def has_double_bar(self):
    #     return self.double_bar_position is not None
    
    has_notes: bool
    is_mm_rest_start: bool
    mm_rest_len: int | None # SHould only be set if MM rest is true
    
    add_line_break: bool = False
    add_page_break: bool = False

# How to represent the extra "visible" measure for MM rests?
# for a MM rest, the first bar is the bar that is displayed, the rest are hidden by musescore
# Solution: have both measures have the same "number"



@dataclass
class Part:
    """
    Reduced Part Class to represent key information for a part
    """

    name: str
    measures: list[Measure]         # Only contains MM rest measures as 1 measure. 


@dataclass
class Score:
    """
    Reduced Score Class to represent key information for a score
    """

    title: str
    subtitle: str | None
    composer: str | None
    lyricist: str | None

    # Broadway stuff
    show_number: str | None
    show_subtitle: str | None

    parts: list[Part]