import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Tuple

from PIL import Image

from barks_fantagraphics.comics_utils import get_abbrev_path

BIG_NUM = 10000


def get_min_max_panel_values(segment_info: Dict[str, Any]) -> Tuple[int, int, int, int]:
    x_min = BIG_NUM
    y_min = BIG_NUM
    x_max = 0
    y_max = 0
    for segment in segment_info["panels"]:
        x0 = segment[0]
        y0 = segment[1]
        w = segment[2]
        h = segment[3]
        x1 = x0 + (w - 1)
        y1 = y0 + (h - 1)
        if x_min > x0:
            x_min = x0
        if x_max < x1:
            x_max = x1
        if y_min > y0:
            y_min = y0
        if y_max < y1:
            y_max = y1

    assert x_min != BIG_NUM
    assert y_min != BIG_NUM
    assert x_max != 0
    assert y_max != 0

    return x_min, y_min, x_max, y_max


class KumikoPanelSegmentation:
    def __init__(self, work_dir: str):
        self.__work_dir = work_dir

    def get_panels_segment_info(self, srce_image: Image, srce_filename: str) -> Dict[str, Any]:
        logging.debug(
            f'Getting panel bounding box for "{get_abbrev_path(srce_filename)}" using kumiko.'
        )

        work_filename = str(
            os.path.join(
                self.__work_dir,
                os.path.splitext(os.path.basename(srce_filename))[0] + "_orig.jpg",
            )
        )
        srce_image.save(work_filename, optimize=True, compress_level=9)
        logging.debug(f'Saved srce image to work file "{work_filename}".')

        logging.debug(f'Getting segment info for "{work_filename}".')
        segment_info = self.__run_kumiko(work_filename)

        return segment_info

    @staticmethod
    def __run_kumiko(page_filename: str) -> Dict[str, Any]:
        kumiko_home_dir = os.path.join(str(Path.home()), "Prj/github/kumiko")
        kumiko_python_path = os.path.join(kumiko_home_dir, ".venv/bin/python3")
        kumiko_script_path = os.path.join(kumiko_home_dir, "kumiko")
        run_args = [kumiko_python_path, kumiko_script_path, "-i", page_filename]
        logging.debug(f"Running kumiko: {' '.join(run_args)}.")
        result = subprocess.run(
            run_args,
            capture_output=True,
            text=True,
            check=True,
        )

        segment_info = json.loads(result.stdout)
        assert len(segment_info) == 1

        return segment_info[0]
