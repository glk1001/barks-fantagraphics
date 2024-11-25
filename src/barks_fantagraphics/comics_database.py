import logging
import os
from pathlib import Path
from typing import List

from .comic_book import ComicBook, get_comic_book
from .comics_info import get_all_comic_book_info
from .consts import STORY_TITLES_DIR


def get_default_comics_database_dir() -> str:
    return str(Path(__file__).parent.parent.parent.absolute())


class ComicsDatabase:
    def __init__(self, database_dir: str):
        self._database_dir = _get_comics_database_dir(database_dir)
        self._story_titles_dir = _get_story_titles_dir(self._database_dir)
        self._all_comic_book_info = get_all_comic_book_info(self._database_dir)

    def get_comics_database_dir(self) -> str:
        return self._database_dir

    def get_story_titles_dir(self) -> str:
        return self._story_titles_dir

    def get_comic_book(self, story_title: str) -> ComicBook:
        return get_comic_book(self._all_comic_book_info, self.get_ini_file(story_title))

    def get_ini_file(self, story_title: str) -> str:
        return os.path.join(self._story_titles_dir, story_title + ".ini")

    def get_all_story_titles(self) -> List[str]:
        possible_ini_files = [f for f in os.listdir(self._story_titles_dir) if f.endswith(".ini")]

        story_titles = []
        for file in possible_ini_files:
            ini_file = os.path.join(self._story_titles_dir, file)
            if os.path.islink(ini_file):
                logging.debug(f'Skipping ini file symlink in "{ini_file}".')
                continue
            story_title = Path(ini_file).stem
            story_titles.append(story_title)

        return sorted(story_titles)


def _get_comics_database_dir(db_dir: str) -> str:
    real_db_dir = os.path.realpath(db_dir)

    if not os.path.isdir(real_db_dir):
        raise Exception(f'Could not find comics database directory "{real_db_dir}".')

    return real_db_dir


def _get_story_titles_dir(db_dir: str) -> str:
    story_titles_dir = os.path.join(db_dir, STORY_TITLES_DIR)

    if not os.path.isdir(story_titles_dir):
        raise Exception(f'Could not find story titles directory "{story_titles_dir}".')

    return story_titles_dir
