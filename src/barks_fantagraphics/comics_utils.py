import os
from typing import List

from .comic_book import ComicBook
from .comics_consts import PageType

STORY_PAGE_TYPES = [
    PageType.COVER,
    PageType.BODY,
    PageType.FRONT_MATTER,
    PageType.BACK_MATTER,
]


def get_story_files(image_dir: str, comic: ComicBook, file_ext: str) -> List[str]:
    return get_story_files_of_page_type(image_dir, comic, file_ext, STORY_PAGE_TYPES)


def get_story_files_of_page_type(
    image_dir: str, comic: ComicBook, file_ext: str, page_types: List[PageType]
) -> List[str]:
    srce_pages = comic.page_images_in_order
    all_files = []
    for page in srce_pages:
        if page.page_type in page_types:
            all_files.append(os.path.join(image_dir, page.page_filenames + file_ext))

    return all_files


def get_abbrev_jpg_page_list(comic: ComicBook) -> List[str]:
    return get_abbrev_jpg_page_of_type_list(comic, STORY_PAGE_TYPES)


def get_abbrev_jpg_page_of_type_list(comic: ComicBook, page_types: List[PageType]) -> List[str]:
    all_pages = []
    for page in comic.config_page_images:
        if page.page_type in page_types:
            all_pages.append(page.page_filenames)

    return all_pages


def get_jpg_page_list(comic: ComicBook) -> List[str]:
    return get_jpg_page_of_type_list(comic, STORY_PAGE_TYPES)


def get_jpg_page_of_type_list(comic: ComicBook, page_types: List[PageType]) -> List[str]:
    all_pages = []
    for page in comic.page_images_in_order:
        if page.page_type in page_types:
            all_pages.append(page.page_filenames)

    return all_pages
