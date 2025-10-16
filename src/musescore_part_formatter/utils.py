# Utils file contains barebones definitions
# Like adding page breaks and adding styles and stuff that is not logic based

from enum import Enum
import xml.etree.ElementTree as ET

from logging import getLogger

# ENUMS and CONSTANTS

# TODO[SC-42]: Make this a function of the time signature somehow?
NUM_MEASURES_PER_LINE = 6
NUM_LINES_PER_PAGE = 8

CONDUCTOR_SCORE_PART_NAME = "CONDUCTOR SCORE"

BROADWAY_SCORE_STYLE_PATH = "src/part_formatter/resources/broadway_score.mss"
BROADWAY_PART_STYLE_PATH = "src/part_formatter/resources/broadway_part.mss"

JAZZ_SCORE_STYLE_PATH = "src/part_formatter/resources/jazz_score.mss"
JAZZ_PART_STYLE_PATH = "src/part_formatter/resources/jazz_part.mss"


class Style(Enum):
    BROADWAY = "broadway"
    JAZZ = "jazz"


LOGGER = getLogger("PartFormatter")

# HELPER FNS


def _make_show_number_text(show_number: str) -> ET.Element:
    txt = ET.Element("Text")
    style = ET.SubElement(txt, "style")
    style.text = "user_2"
    text = ET.SubElement(txt, "text")
    text.text = show_number
    return txt


def _make_show_title_text(show_title: str) -> ET.Element:
    txt = ET.Element("Text")
    style = ET.SubElement(txt, "style")
    style.text = "user_3"
    text = ET.SubElement(txt, "text")
    text.text = show_title
    return txt


def _make_part_name_text(part_name: str) -> ET.Element:
    txt = ET.Element("Text")
    style = ET.SubElement(txt, "style")
    style.text = "instrument_excerpt"
    text = ET.SubElement(txt, "text")
    text.text = part_name
    return txt


def _make_line_break() -> ET.Element:
    lb = ET.Element("LayoutBreak")
    subtype = ET.SubElement(lb, "subtype")
    subtype.text = "line"
    return lb


def _make_page_break() -> ET.Element:
    pb = ET.Element("LayoutBreak")
    subtype = ET.SubElement(pb, "subtype")
    subtype.text = "page"
    return pb


def _make_double_bar() -> ET.Element:
    db = ET.Element("BarLine")
    subtype = ET.SubElement(db, "subtype")
    subtype.text = "double"
    linked = ET.SubElement(db, "Linked")
    linked.text = "\n"
    return db


def _add_line_break_to_measure(measure: ET.Element) -> None:
    index = 0
    for elem in measure:
        if elem.tag == "voice":
            break
        index += 1
    measure.insert(index, _make_line_break())


def _measure_has_line_break(measure: ET.Element) -> bool:
    return measure.find("LayoutBreak") is not None


def _add_line_break_to_measure_opt(measure: ET.Element) -> None:
    if not _measure_has_line_break(measure):
        _add_line_break_to_measure(measure)


def _add_page_break_to_measure(measure: ET.Element) -> None:
    # if line break already there, replace with a page break
    if measure.find("LayoutBreak") is not None:
        measure.find("LayoutBreak").find("subtype").text = "page"
        return

    LOGGER.warning("added a page break to a bar that did not have a line break!")
    index = 0
    for elem in measure:
        if elem.tag == "voice":
            break
        index += 1

    measure.insert(index, _make_page_break())


def _add_double_bar_to_measure(measure: ET.Element) -> None:
    # Add the double bar as the very last tag in the measure
    measure.append(_make_double_bar())

def _measure_has_double_bar(measure: ET.Element) -> bool:
    return measure.find("BarLine") is not None

def _measure_has_rehearsal_mark(measure: ET.Element) -> bool:
    #TODO: Check if find also checks in sub-elements (eg. Voice tag)
    return measure.find("RehearsalMark") is not None