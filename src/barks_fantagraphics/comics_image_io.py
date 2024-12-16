from typing import Dict

from PIL import Image
from PIL.PngImagePlugin import PngInfo

Image.MAX_IMAGE_PIXELS = None

SAVE_PNG_COMPRESSION = 9
SAVE_JPG_QUALITY = 95
SAVE_JPG_COMPRESS_LEVEL = 9

METADATA_PROPERTY_GROUP = "BARKS"


def add_jpg_metadata(jpg_file: str, metadata: Dict[str, str]):
    pil_image = Image.open(jpg_file, "r")

    jpg_metadata = PngInfo()
    for key in metadata:
        jpg_metadata.add_text(f"{METADATA_PROPERTY_GROUP}:{key}", metadata[key])

    pil_image.save(
        jpg_file,
        jpginfo=jpg_metadata,
        optimize=True,
        compress_level=SAVE_JPG_COMPRESS_LEVEL,
        quality=SAVE_JPG_QUALITY,
    )


def add_png_metadata(png_file: str, metadata: Dict[str, str]):
    pil_image = Image.open(png_file, "r")

    png_metadata = PngInfo()
    for key in metadata:
        png_metadata.add_text(f"{METADATA_PROPERTY_GROUP}:{key}", metadata[key])

    pil_image.save(
        png_file, pnginfo=png_metadata, optimize=True, compress_level=SAVE_PNG_COMPRESSION
    )


def get_png_metadata(png_file: str) -> Dict[str, str]:
    pil_image = Image.open(png_file, "r")

    png_metadata = pil_image.info

    prefix = METADATA_PROPERTY_GROUP + ":"
    metadata = dict()
    for key in png_metadata:
        if key.startswith(prefix):
            metadata[key[len(prefix) :]] = png_metadata[key]

    return metadata


def get_jpg_metadata(jpg_file: str) -> Dict[str, str]:
    pil_image = Image.open(jpg_file, "r")

    jpg_comments = pil_image.app["COM"]

    metadata = dict()
    metadata["comments"] = jpg_comments

    return metadata
