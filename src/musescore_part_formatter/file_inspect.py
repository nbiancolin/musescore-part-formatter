"""
A collection of functions designed to quickly look into a file and get key data
"""

from typing import TypedDict
import shutil
import tempfile
import zipfile
import os

import xml.etree.ElementTree as ET


class ScoreInfo(TypedDict):
    title: str
    meta_title: str
    subtitle: str
    meta_subtitle: str
    composer: str
    meta_composer: str
    meta_arranger: str
    lyricist: str
    meta_lyricist: str
    part_name: str

    num_instruments: int
    num_staves: int


TITLE_BOX_PROPERTIES = [
    "title",
    "subtitle",
    "composer",
    "lyricist",
]
META_PROPERTIES = ["arranger", "composer", "workTitle", "subtitle"]


def get_properties_from_title_box(score: ET.Element, debug=False) -> dict["str", "str"]:
    staff = score.find("Staff")
    assert staff is not None, "Couldnt find staff -- malformed mscx file"
    vbox = staff.find("VBox")
    if debug:
        assert vbox is not None, "Couldnt find vbox"
    if vbox is None:
        return {}

    res = {}

    for text_elem in vbox.findall("Text"):
        res[text_elem.find("style").text] = text_elem.find("text").text

    return res


def get_score_properties_from_meta(score: ET.Element) -> dict["str", "str"]:
    metatags = score.findall("metaTag")
    res = {}
    for tag in metatags:
        if tag.attrib.get("name") in META_PROPERTIES:
            res[f"meta_{tag.attrib.get('name')}"] = tag.text

    return res


def get_num_staves(score: ET.Element) -> int:
    return len(score.findall("Staff"))


def get_num_instruments(score: ET.Element) -> int:
    return len(score.findall("Part"))


def get_time_signatures(score: ET.Element) -> list[str]:
    staff = score.find("Staff")
    assert staff is not None, "Couldnt find staff -- malformed mscx file"
    measures = staff.findall("Measure")
    res = []
    for measure in measures:
        if time_sig := measure.find("voice").find("TimeSig"):
            res.append(f'{time_sig.find("sigN").text}/{time_sig.find("sigD").text}')
    return res



def get_all_properties(score: ET.Element) -> ScoreInfo:
    res = get_properties_from_title_box(score) | get_score_properties_from_meta(score)
    return res
