import os
from pathlib import Path
from typing import Union

from .comics_consts import BARKS_ROOT_DIR


def get_relpath(file: Union[str, Path]) -> str:
    if str(file).startswith(BARKS_ROOT_DIR):
        return os.path.relpath(file, BARKS_ROOT_DIR)

    file_parts = Path(file).parts[-2:]
    return str(os.path.join(*file_parts))


def get_clean_path(file: Union[str, Path]) -> str:
    return str(file).replace(str(Path.home()), "$HOME")
