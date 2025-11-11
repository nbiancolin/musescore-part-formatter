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
    new_add_page_breaks,
    cleanup_mm_rests,
    add_broadway_header,
    add_part_name,
)

from logging import getLogger

import argparse
import sys


LOGGER = getLogger("PartFormatter")


class FormattingParams(TypedDict):
    selected_style: str | None
    show_title: str | None
    show_number: str | None
    version_num: str | None
    num_measures_per_line_score: int | None
    num_measures_per_line_part: int | None
    num_lines_per_page: int | None


def format_mscx(
    mscx_path: str, params: FormattingParams, is_part: bool = False
) -> bool:
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
            "versionNum": params.get("version_num", "v1.0.0")
        }

        # set score properties
        for metaTag in score.findall("metaTag"):
            for k in score_properties.keys():
                if metaTag.attrib.get(k):
                    metaTag.attrib[k] = score_properties[k]

        staves = score.findall("Staff")

        staff = staves[0]  # noqa  -- only add layout breaks to the first staff
        prep_mm_rests(
            staff,
        )
        add_rehearsal_mark_line_breaks(staff)
        add_double_bar_line_breaks(staff)
        if is_part:
            # TODO[SC-181]: move defaults to utils.py
            add_regular_line_breaks(staff, params.get("num_measures_per_line_part", 6))
        else:
            add_regular_line_breaks(staff, params.get("num_measures_per_line_score", 4))
        final_pass_through(staff)
        new_add_page_breaks(staff, params.get("num_lines_per_page", 7))
        cleanup_mm_rests(staff)
        if params.get("selected_style") == Style.BROADWAY:
            add_broadway_header(
                staff, params.get("show_number"), params.get("show_title")
            )
        add_part_name(staff)

        with open(mscx_path, "wb") as f:
            ET.indent(tree, space="  ", level=0)
            tree.write(f, encoding="utf-8", xml_declaration=True)
        LOGGER.info(f"Output written to {mscx_path}")
        return True

    except FileNotFoundError:
        LOGGER.warning(f"Error: File '{mscx_path}' not found.")
        return False


def format_mscz(input_path: str, output_path: str, params: FormattingParams) -> bool:
    """
    Takes in a (compressed) musescore file, processes it, and outputs it to the path specified by `output_path`

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
            LOGGER.warning("No .mscx files found in the provided mscz file.")
            shutil.rmtree(work_dir)
            return False

        for mscx_path in mscx_files:
            LOGGER.info(f"Processing {mscx_path}...")
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


def main():
    """
    Command-line interface for formatting MuseScore files (.mscz).
    Example:
        python -m musescore_part_formatter.main input.mscz output.mscz \
            --style broadway \
            --show-title "My Song" \
            --show-number "01" \
            --num-measures-per-line-score 4 \
            --num-measures-per-line-part 6 \
            --num-lines-per-page 7
    """
    parser = argparse.ArgumentParser(description="Format a MuseScore file (.mscz).")

    parser.add_argument("input", help="Path to input .mscz file")
    parser.add_argument("output", help="Path to output .mscz file")
    parser.add_argument(
        "--style",
        dest="selected_style",
        default="broadway",
        help="Style to apply (default: broadway)",
    )
    parser.add_argument(
        "--show-title", dest="show_title", default=None, help="Title to display"
    )
    parser.add_argument(
        "--show-number", dest="show_number", default=None, help="Number to display"
    )
    parser.add_argument(
        "--version-num", dest="version_num", default=None, help="Version Num to display"
    )
    parser.add_argument(
        "--num-measures-per-line-score",
        type=int,
        default=4,
        help="Number of measures per line in the full score (default: 4)",
    )
    parser.add_argument(
        "--num-measures-per-line-part",
        type=int,
        default=6,
        help="Number of measures per line in parts (default: 6)",
    )
    parser.add_argument(
        "--num-lines-per-page",
        type=int,
        default=7,
        help="Number of lines per page (default: 7)",
    )

    args = parser.parse_args()

    params: FormattingParams = {
        "selected_style": args.selected_style,
        "show_title": args.show_title,
        "show_number": args.show_number,
        "version_num": args.version_num,
        "num_measures_per_line_score": args.num_measures_per_line_score,
        "num_measures_per_line_part": args.num_measures_per_line_part,
        "num_lines_per_page": args.num_lines_per_page,
    }

    try:
        success = format_mscz(args.input, args.output, params)
        if success:
            print(f"✅ Successfully formatted score: {args.output}")
        else:
            print("⚠️ Formatting failed. See logs for details.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
