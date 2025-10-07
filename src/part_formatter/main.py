from typing import TypedDict
import shutil
import tempfile
import zipfile
import os

import xml.etree.ElementTree as ET

from .utils import Style
from .formatting import add_styles_to_score_and_parts
from .formatting import (
    prep_mm_rests,
    add_rehearsal_mark_line_breaks,
    add_double_bar_line_breaks,
    add_regular_line_breaks,
    final_pass_through,
    add_page_breaks,
    cleanup_mm_rests,
    add_broadway_header,
    add_part_name,
)


class FormattingParams(TypedDict):
    selected_style: str | None
    show_title: str | None
    show_number: str | None
    num_measures_per_line_score: int | None
    num_measures_per_line_part: int | None


def format_mscx(mscx_path: str, params: FormattingParams, is_part:bool = False) -> bool:
    """
    Takes in an (uncompressed) musescore file, processes it, and outputs it in place
    This is usually only used internally by `format_mscz()`, but if the user wants to format a mscx file, why not let them?

    Returns:
    - True if processing completed successfully
    - False if an error occurred

    TODO: Remove when complete:
    May also raise exceptions while we are in this development phase
    """
    try:
        parser = ET.XMLParser()
        tree = ET.parse(mscx_path, parser)
        root = tree.getroot()
        score = root.find("Score")
        if score is None:
            raise ValueError("No <Score> tag found in the XML.")

        score_properties = {
            "albumTitle": params.get("show_title", ""),
            "trackNum": params.get("show_number", ""),
        }

        # set score properties
        for metaTag in score.findall("metaTag"):
            for k in score_properties.keys():
                if metaTag.attrib.get(k):
                    metaTag.attrib[k] = score_properties[k]

        staves = score.findall("Staff")

        staff = staves[0]  # noqa  -- only add layout breaks to the first staff
        prep_mm_rests(staff)
        add_rehearsal_mark_line_breaks(staff)
        add_double_bar_line_breaks(staff)
        if is_part:
            add_regular_line_breaks(
                staff, params.get("num_measures_per_line_part", 6)
            ) 
        else:
            add_regular_line_breaks(
                staff, params.get("num_measures_per_line_score", 4)
            ) 
        final_pass_through(staff)
        # add_page_breaks(staff)
        cleanup_mm_rests(staff)
        if params.get("selected_style") == Style.BROADWAY:
            add_broadway_header(
                staff, params.get("show_number"), params.get("show_title")
            )
        add_part_name(staff)

        with open(mscx_path, "wb") as f:
            ET.indent(tree, space="  ", level=0)
            tree.write(f, encoding="utf-8", xml_declaration=True)
        print(f"Output written to {mscx_path}")

    except FileNotFoundError:
        print(f"Error: File '{mscx_path}' not found.")
        return False


def format_mscz(input_path: str, output_path: str, params: FormattingParams) -> bool:
    """
    Takes in a (compressed) musescore file, processes it, and outputs it to the path specified by `output_path`

    Kwargs are for customizable options
    TODO: Maybe take them in directly

    Returns:
    - True if processing completed successfully
    - False if an error occurred

    TODO: Remove when complete:
    May also raise exceptions while we are in this development phase
    """

    # unpack params
    style_name = (
        params["selected_style"] if params.get("selected_style") else "broadway"
    )

    with tempfile.TemporaryDirectory() as work_dir:
        with zipfile.ZipFile(input_path, "r") as zip_ref:
            # Extract all files to "temp" and collect all .mscx files from the zip structure
            zip_ref.extractall(work_dir)

        selected_style = Style(style_name)

        add_styles_to_score_and_parts(selected_style, work_dir)

        mscx_files = [
            os.path.join(work_dir, f) for f in zip_ref.namelist() if f.endswith(".mscx")
        ]
        if not mscx_files:
            print("No .mscx files found in the provided mscz file.")
            shutil.rmtree(work_dir)
            return False

        for mscx_path in mscx_files:
            #TODO[]: Convert all prints to Logs
            print(f"Processing {mscx_path}...")
            if "Excerpts" in mscx_path:
                format_mscx(mscx_path, params, is_part=True)
            else:
                format_mscx(mscx_path, params, is_part=False)

        with zipfile.ZipFile(output_path, "w") as zip_out:
            for root, _, files in os.walk(work_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_out.write(file_path, os.path.relpath(file_path, work_dir))

    return True
