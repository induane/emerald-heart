from __future__ import annotations

import logging
import pathlib
from io import BytesIO

from boltons.ioutils import SpooledBytesIO
from django.conf import settings
from PIL import Image as PILImage
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import ImageFileDirectory_v2

from emerald_heart.hints import BinaryWritableFile

LOG = logging.getLogger(__name__)
MEDIA_DIR = pathlib.Path(__file__).absolute().parent.joinpath("media")
REVERSED_TAGS = {v: k for k, v in TAGS.items()}


def get_exif(artist: str) -> bytes:
    """Return a simple set of exif data - artist only."""
    ifd = ImageFileDirectory_v2()
    ifd[REVERSED_TAGS["Artist"]] = artist
    ifd[REVERSED_TAGS["LightSource"]] = 1  # Always sets value to dayLight
    out = BytesIO()
    ifd.save(out)
    return b"Exif\x00\x00" + out.getvalue()


def set_exif(*, flo: BinaryWritableFile, artist: str, fmt: str = "PNG") -> BinaryWritableFile:
    """Set exif artist data on a given file."""
    exif_data = get_exif(artist)
    pos = flo.tell()  # Stash the original read head position
    flo.seek(0)
    try:
        with PILImage.open(flo) as tmp:
            pil_img = tmp.copy()
    except Exception:
        flo.seek(pos)  # Return read head to original position
        LOG.exception("Could not open image file.")
        raise

    flo.seek(0)
    pil_img.save(flo, optimize=True, exif=exif_data, format=fmt)
    flo.seek(0)
    return flo


def generate_thumbnail(
    flo: BinaryWritableFile, size: int = settings.THUMBNAIL_SIZE, artist: str | None = None
) -> bytes:
    """Convert an image file to a thumbnail."""
    dimensions = (size, size)
    pos = flo.tell()  # Stash the original read head position
    flo.seek(0)
    try:
        image = PILImage.open(flo)
    except Exception:
        flo.seek(pos)  # Return read head to original position
        LOG.exception("Could not open image file.")
        raise

    image.thumbnail(dimensions, PILImage.ANTIALIAS)
    with SpooledBytesIO() as t:
        thumb = PILImage.new("RGB", dimensions, (255, 255, 255))
        dest_size = (
            int((dimensions[0] - image.size[0]) / 2),
            int((dimensions[1] - image.size[1]) / 2),
        )
        try:
            mask = image.split()[3]
        except IndexError:
            thumb.paste(image, dest_size)
        else:
            thumb.paste(image, dest_size, mask=mask)
        thumb.save(t, format="JPEG")
        flo.seek(pos)  # Return read head to original position
        if artist:
            alt_flo = set_exif(flo=t, artist=artist, fmt="JPEG")
            pos = alt_flo.tell()
            alt_flo.seek(0)
            try:
                image_bytes = alt_flo.read()
            except Exception:
                alt_flo.seek(pos)
                raise
            alt_flo.seek(pos)
        else:
            image_bytes = t.getvalue()
    if not isinstance(image_bytes, bytes):
        raise TypeError(f"Expected to yield bytes but file-like-object returned {type(image_bytes)} instead")
    return image_bytes


def scale_pil(img: PILImage, width: int) -> PILImage.Image:
    """Scale a PIL image instance."""
    original_width, original_height = img.size

    # Figure out what percent of original width the new width is
    percent = width / float(original_width)

    # Calculate new height
    new_height = int(float(original_height) * percent)

    # Get a resized image of decent quality
    return img.resize((width, new_height), resample=PILImage.Resampling.BICUBIC)


def get_size(flo: BinaryWritableFile) -> tuple[int, int]:
    """Get the size in pixels for the given file or file-like-object."""
    pos = flo.tell()  # Stash the original read head position
    flo.seek(0)
    try:
        with PILImage.open(flo) as tmp:
            width, height = tmp.size
        return (int(width), int(height))
    except Exception:
        flo.seek(pos)  # Return read head to original position
        LOG.exception("Could not open image file.")
        raise


def scale_flo(flo: BinaryWritableFile, width: int, fmt: str = "JPEG") -> SpooledBytesIO:
    """
    Scale an image to a given width, preserving the aspect ratio.

    :param flo: an image file
    :param int: size of thumbnail to generate
    :returns: scaled image as bytes in jpeg format
    """
    pos = flo.tell()  # Stash the original read head position
    flo.seek(0)

    try:
        with PILImage.open(flo) as tmp:
            img_copy = tmp.copy()
    except Exception:
        flo.seek(pos)  # Return read head to original position
        LOG.exception("Could not open image file.")
        raise
    flo.seek(pos)

    try:
        new_image = scale_pil(img_copy, width)
    except Exception:
        LOG.exception("Unable to scale image file")
        raise

    # Convert to RGB if we got an image with an alpha channel when our output is JPEG
    if new_image.mode in ("RGBA", "P") and fmt in ("JPG", "JPEG"):
        new_image = new_image.convert("RGB")

    # We don't want to modify the original image; create a new one to write to
    scaled = SpooledBytesIO()
    new_image.save(scaled, optimize=True, format=fmt)
    scaled.seek(0)
    return scaled
