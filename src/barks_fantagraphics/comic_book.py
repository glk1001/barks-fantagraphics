import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .comics_consts import (
    PageType,
    IMAGES_SUBDIR,
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    THE_COMICS_DIR,
    THE_YEARS_COMICS_DIR,
    INSET_FILE_EXT,
)
from .comics_info import (
    ISSUE_NAME_AS_TITLE,
    MONTH_AS_LONG_STR,
    SHORT_ISSUE_NAME,
    SILENT_NIGHT,
    SILENT_NIGHT_PUBLICATION_ISSUE,
    ComicBookInfo,
    SourceBook,
    get_formatted_day,
)

INTRO_TITLE_DEFAULT_FONT_SIZE = 155
INTRO_AUTHOR_DEFAULT_FONT_SIZE = 90


@dataclass
class OriginalPage:
    page_filenames: str
    page_type: PageType


@dataclass
class RequiredDimensions:
    panels_bbox_width: int = -1
    panels_bbox_height: int = -1
    page_num_y_bottom: int = -1


@dataclass
class ComicBook:
    ini_file: str
    title: str
    title_font_file: str
    title_font_size: int
    # NOTE: Need 'issue_title' to force a series title that has
    #       changed from another title. E.g., FC 495 == Uncle Scrooge #3
    issue_title: str
    file_title: str
    author_font_size: int
    srce_min_panels_bbox_width: int
    srce_max_panels_bbox_width: int
    srce_min_panels_bbox_height: int
    srce_max_panels_bbox_height: int
    srce_av_panels_bbox_width: int
    srce_av_panels_bbox_height: int
    required_dim: RequiredDimensions
    fanta_info: SourceBook
    srce_dir: str
    srce_fixes_dir: str
    srce_upscayled_dir: str
    srce_restored_dir: str
    srce_restored_fixes_dir: str  # TODO: Get rid of this????
    panel_segments_dir: str
    series_name: str
    number_in_series: int
    chronological_number: int
    intro_inset_file: str
    publication_date: str
    submitted_date: str
    submitted_year: int
    publication_text: str
    comic_book_info: ComicBookInfo
    config_page_images: List[OriginalPage]
    page_images_in_order: List[OriginalPage]

    def __post_init__(self):
        assert self.series_name != ""
        assert self.number_in_series > 0

    def get_srce_root_dir(self) -> str:
        return os.path.dirname(self.srce_dir)

    def get_srce_fixes_root_dir(self) -> str:
        return os.path.dirname(self.srce_fixes_dir)

    def get_srce_image_dir(self) -> str:
        return os.path.join(self.srce_dir, IMAGES_SUBDIR)

    def get_srce_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_fixes_dir, IMAGES_SUBDIR)

    def get_srce_upscayled_image_dir(self) -> str:
        return os.path.join(self.srce_upscayled_dir, IMAGES_SUBDIR)

    def get_srce_restored_image_dir(self) -> str:
        return os.path.join(self.srce_restored_dir, IMAGES_SUBDIR)

    def get_srce_restored_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_restored_fixes_dir, IMAGES_SUBDIR)

    def get_srce_segments_root_dir(self) -> str:
        return os.path.dirname(self.panel_segments_dir)

    # TODO: Should dest stuff be elsewhere??
    def get_dest_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIRS_DIR

    def get_dest_dir(self) -> str:
        return os.path.join(
            self.get_dest_root_dir(),
            self.get_dest_rel_dirname(),
        )

    def get_dest_rel_dirname(self) -> str:
        file_title = get_lookup_title(self.title, self.file_title)
        return f"{self.chronological_number:03d} {file_title}"

    def get_series_comic_title(self) -> str:
        return f"{self.series_name} {self.number_in_series}"

    def get_dest_image_dir(self) -> str:
        return os.path.join(self.get_dest_dir(), IMAGES_SUBDIR)

    def get_dest_zip_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIR

    def get_dest_series_zip_symlink_dir(self) -> str:
        return os.path.join(
            THE_COMICS_DIR,
            self.series_name,
        )

    def get_dest_year_zip_symlink_dir(self) -> str:
        return os.path.join(
            THE_YEARS_COMICS_DIR,
            str(self.submitted_year),
        )

    def get_dest_comic_zip_filename(self) -> str:
        return f"{self.get_title_with_issue_num()}.cbz"

    def get_dest_comic_zip(self) -> str:
        return os.path.join(self.get_dest_zip_root_dir(), self.get_dest_comic_zip_filename())

    def get_dest_series_comic_zip_symlink_filename(self) -> str:
        file_title = get_lookup_title(self.title, self.file_title)
        full_title = f"{file_title} [{self.get_comic_issue_title()}]"
        return f"{self.number_in_series:03d} {full_title}.cbz"

    def get_dest_series_comic_zip_symlink(self) -> str:
        return os.path.join(
            f"{self.get_dest_series_zip_symlink_dir()}",
            f"{self.get_dest_series_comic_zip_symlink_filename()}",
        )

    def get_dest_year_comic_zip_symlink(self) -> str:
        return os.path.join(
            f"{self.get_dest_year_zip_symlink_dir()}",
            f"{self.get_dest_comic_zip_filename()}",
        )

    def get_comic_title(self) -> str:
        if self.title != "":
            return self.title
        if self.issue_title != "":
            return self.issue_title

        return self.__get_comic_title_from_issue_name()

    def __get_comic_title_from_issue_name(self) -> str:
        issue_name = self.comic_book_info.issue_name
        if issue_name not in ISSUE_NAME_AS_TITLE:
            issue_name += "\n"
        else:
            issue_name = ISSUE_NAME_AS_TITLE[issue_name] + " #"

        return f"{issue_name}{self.comic_book_info.issue_number}"

    def get_comic_issue_title(self) -> str:
        issue_name = SHORT_ISSUE_NAME[self.comic_book_info.issue_name]
        return f"{issue_name} {self.comic_book_info.issue_number}"

    def get_title_with_issue_num(self) -> str:
        return f"{self.get_dest_rel_dirname()} [{self.get_comic_issue_title()}]"


def get_lookup_title(title: str, file_title: str) -> str:
    if title != "":
        return get_safe_title(title)

    assert file_title != ""
    return file_title


def get_safe_title(title: str) -> str:
    safe_title = title.replace("\n", " ")
    safe_title = safe_title.replace("- ", "-")
    safe_title = safe_title.replace('"', "")
    return safe_title


def get_main_publication_info(
    file_title: str, cb_info: ComicBookInfo, fanta_info: SourceBook
) -> str:
    if file_title == SILENT_NIGHT:
        # Originally intended for WDCS 64
        publication_text = (
            f"(*) Rejected by Western editors in 1945, this story was originally\n"
            f" intended for publication in {get_formatted_first_published_str(cb_info)}\n"
            + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
            + f"\n"
            + f"The story was also not published in the Fantagraphics CBDL but\n"
            + f"fortunately did appear in {SILENT_NIGHT_PUBLICATION_ISSUE}\n"
            + f"Color restoration by {cb_info.colorist}"
        )
        return publication_text

    publication_text = (
        f"First published in {get_formatted_first_published_str(cb_info)}\n"
        + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
        + f"\n"
        + f"This edition published in {fanta_info.pub} CBDL,"
        + f" Volume {fanta_info.volume}, {fanta_info.year}\n"
        + f"Color restoration by {cb_info.colorist}"
    )

    return publication_text


def _get_pages_in_order(config_pages: List[OriginalPage]) -> List[OriginalPage]:
    page_images = []
    for config_page in config_pages:
        if "-" not in config_page.page_filenames:
            page_images.append(config_page)
        else:
            start, end = config_page.page_filenames.split("-")
            start_num = int(start)
            end_num = int(end)
            for file_num in range(start_num, end_num + 1):
                filename = f"{file_num:03d}"
                page_images.append(OriginalPage(filename, config_page.page_type))

    return page_images


def get_inset_file(ini_file: str, file_title: str) -> str:
    prefix = file_title if file_title else Path(ini_file).stem
    inset_filename = prefix + " Inset" + INSET_FILE_EXT
    ini_file_dir = os.path.dirname(ini_file)

    return str(os.path.join(ini_file_dir, inset_filename))


def get_formatted_first_published_str(info: ComicBookInfo) -> str:
    issue = f"{info.issue_name} #{info.issue_number}"

    if info.issue_month == -1:
        issue_date = info.issue_year
    else:
        issue_date = f"{MONTH_AS_LONG_STR[info.issue_month]} {info.issue_year}"

    return f"{issue}, {issue_date}"


def get_formatted_submitted_date(info: ComicBookInfo) -> str:
    if info.submitted_day == -1:
        return f", {MONTH_AS_LONG_STR[info.submitted_month]} {info.submitted_year}"

    return (
        f" on {MONTH_AS_LONG_STR[info.submitted_month]}"
        f" {get_formatted_day(info.submitted_day)}, {info.submitted_year}"
    )
