import argparse
import os
from typing import Tuple, Union

from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir

from barks_fantagraphics.comics_consts import PageType


def get_all_pages_str(comic: ComicBook) -> str:
    all_pages_str = ""
    for page in comic.config_page_images:
        if page.page_type in [PageType.FRONT, PageType.BODY]:
            all_pages_str += page.page_filenames + ", "

    return all_pages_str


COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"


def get_args():
    parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Create a clean Barks comic from Fantagraphics source."
    )

    parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    parser.add_argument(
        VOLUME_ARG,
        action="store",
        type=int,
        required=True,
    )

    args = parser.parse_args()

    return args


cmd_args = get_args()
comics_database = ComicsDatabase(cmd_args.comics_database_dir)

fanta_titles = comics_database.get_all_story_titles_in_fantagraphics_volume(cmd_args.volume)
for title in fanta_titles:
    comic_book = comics_database.get_comic_book(title)
    print(f'Title: "{title}", pages: {get_all_pages_str(comic_book)}')
