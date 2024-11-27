import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from typing import List, Tuple

from .comic_book import ComicBook, get_comic_book
from .comics_consts import STORY_TITLES_DIR, BARKS_ROOT_DIR
from .comics_info import get_all_comic_book_info, SOURCE_COMICS


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
        ini_files = [f for f in os.listdir(self._story_titles_dir) if f.endswith(".ini")]

        story_titles = []
        for ini_file in ini_files:
            story_title = Path(ini_file).stem
            story_titles.append(story_title)

        return sorted(story_titles)

    def get_all_story_titles_in_fantagraphics_volume(self, volume_num: int) -> List[str]:
        ini_files = [f for f in os.listdir(self._story_titles_dir) if f.endswith(".ini")]

        config = ConfigParser(interpolation=ExtendedInterpolation())
        fanta_key = f"FANTA_{volume_num:02}"
        story_titles = []
        for file in ini_files:
            ini_file = os.path.join(self._story_titles_dir, file)
            config.read(ini_file)
            if config["info"]["source_comic"] == fanta_key:
                story_title = Path(ini_file).stem
                story_titles.append(story_title)

        return sorted(story_titles)

    # "$HOME/Books/Carl Barks/Fantagraphics/Carl Barks Vol. 2 - Donald Duck - Frozen Gold"
    #     root_dir = "$HOME/Books/Carl Barks/Fantagraphics"
    #     subdir = "Fantagraphics"
    #     title = "Carl Barks Vol. 2 - Donald Duck - Frozen Gold"
    def _get_fantagraphics_root_dir_sub_dir_and_title(
        self, volume_num: int
    ) -> Tuple[str, str, str]:
        fanta_key = f"FANTA_{volume_num:02}"
        fanta_info = SOURCE_COMICS[fanta_key]
        return (
            str(os.path.join(BARKS_ROOT_DIR, fanta_info.subdir)),
            fanta_info.subdir,
            fanta_info.title,
        )

    def get_fantagraphics_root_dir(self, volume_num: int) -> str:
        return self._get_fantagraphics_root_dir_sub_dir_and_title(volume_num)[0]

    def get_fantagraphics_volume_subdir(self, volume_num: int) -> str:
        return self._get_fantagraphics_root_dir_sub_dir_and_title(volume_num)[1]

    def get_fantagraphics_volume_dir(self, volume_num: int) -> str:
        srce_root_dir, _, title = self._get_fantagraphics_root_dir_sub_dir_and_title(volume_num)
        return os.path.join(srce_root_dir, title)


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
