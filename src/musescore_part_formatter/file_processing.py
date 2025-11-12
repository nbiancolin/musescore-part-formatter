"""
Collection of code to deal with unpacking and re-packing mscz files
(so that it can be reused between the part formatter and the introspector)
"""

from contextlib import contextmanager
from typing import Iterator, List, Tuple
import tempfile
import zipfile
import os
from logging import getLogger

LOGGER = getLogger(__name__)

@contextmanager
def unpack_mscz_to_tempdir(mscz_path: str) -> Iterator[Tuple[str, List[str]]]:
    """
    Unpack a .mscz (zip) into a temporary directory and yield (work_dir, mscx_files).
    Cleans up the tempdir automatically when the context exits.
    """
    with tempfile.TemporaryDirectory() as work_dir:
        try:
            with zipfile.ZipFile(mscz_path, "r") as z:
                z.extractall(work_dir)
                mscx_files = [
                    os.path.join(work_dir, name)
                    for name in z.namelist()
                    if name.endswith(".mscx")
                ]
            yield work_dir, mscx_files
        except Exception:
            LOGGER.exception("Failed to unpack %s", mscz_path)
            # re-raise so callers can handle the failure
            raise