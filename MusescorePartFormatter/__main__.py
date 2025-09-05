from typing import TypedDict
import shutil
import tempfile
import zipfile
import os

from utils import Style

class FormattingParams(TypedDict):
    show_title: str|None
    show_number: str|None
    num_measures_per_line_score: int|None
    num_measures_per_line_part: int|None

def format_mscx(input_path: str, params: FormattingParams) -> bool:
    """
    Takes in an (uncompressed) musescore file, processes it, and outputs it in place
    This is usually only used internally by `format_mscz()`, but if the user wants to format a mscx file, why not let them?

    Returns:
    - True if processing completed successfully
    - False if an error occurred

    TODO: Remove when complete:
    May also raise exceptions while we are in this development phase 
    """

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
            print(f"Processing {mscx_path}...")
            format_mscx(
                mscx_path,
                params
            )

        with zipfile.ZipFile(output_path, "w") as zip_out:
            for root, _, files in os.walk(work_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_out.write(file_path, os.path.relpath(file_path, work_dir))


    return True
