import os
from datetime import datetime
from pathlib import Path
from typing import Union

from .comics_consts import BARKS_ROOT_DIR


def get_work_dir(work_dir_root: str) -> str:
    os.makedirs(work_dir_root, exist_ok=True)
    if not os.path.isdir(work_dir_root):
        raise Exception(f'Could not find work root directory "{work_dir_root}".')

    work_dir = os.path.join(work_dir_root, datetime.now().strftime("%Y_%m_%d-%H_%M_%S.%f"))
    os.makedirs(work_dir)

    return work_dir


def get_relpath(file: Union[str, Path]) -> str:
    if str(file).startswith(BARKS_ROOT_DIR):
        return os.path.relpath(file, BARKS_ROOT_DIR)

    file_parts = Path(file).parts[-2:]
    return str(os.path.join(*file_parts))


def get_abspath_from_relpath(relpath: str, root_dir=BARKS_ROOT_DIR) -> str:
    if os.path.isabs(relpath):
        return relpath
    return os.path.join(root_dir, relpath)


def get_clean_path(file: Union[str, Path]) -> str:
    return str(file).replace(str(Path.home()), "$HOME")


def get_timestamp(file: str) -> float:
    if os.path.islink(file):
        return os.lstat(file).st_mtime

    return os.path.getmtime(file)


def get_timestamp_str(file: str) -> str:
    return get_timestamp_as_str(get_timestamp(file))


def get_timestamp_as_str(timestamp: float) -> str:
    timestamp_as_date = datetime.fromtimestamp(timestamp)
    timestamp_as_date_as_str = timestamp_as_date.strftime("%Y_%m_%d-%H_%M_%S.%f")
    return timestamp_as_date_as_str[:-4]  # trim microseconds to two places


def dest_file_is_older_than_srce(srce_file: str, dest_file: str, include_missing_dest=True) -> bool:
    if include_missing_dest and not os.path.exists(dest_file):
        return True

    srce_timestamp = get_timestamp(srce_file)
    dest_timestamp = get_timestamp(dest_file)

    return srce_timestamp > dest_timestamp


def file_is_older_than_timestamp(file: str, timestamp: float) -> bool:
    file_timestamp = get_timestamp(file)

    return file_timestamp > timestamp
