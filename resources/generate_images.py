from __future__ import annotations

import errno
import os
import shutil
import sys
from os.path import dirname as p_dir

from emerald_heart.utils import image

SQUARE_SIZES = {
    "favicon.ico": 16,
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-icon-57x57.png": 57,
    "apple-icon-60x60.png": 60,
    "ms-icon-70x70.png": 70,
    "apple-icon-72x72.png": 72,
    "apple-icon-76x76.png": 76,
    "favicon-96x96.png": 96,
    "apple-icon-114x114.png": 114,
    "apple-icon-120x120.png": 120,
    "apple-icon-144x144.png": 144,
    "ms-icon-144x144.png": 144,
    "ms-icon-150x150.png": 150,
    "apple-icon-152x152.png": 152,
    "apple-icon-180x180.png": 180,
    "favicon-192x192.png": 192,
    "ms-icon-310x310.png": 310,
}
BASE_DIR = p_dir(os.path.abspath(__file__))
FORMAT_MAP = {
    ".ico": "ICO",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
}


def generate_images() -> None:
    """Given an image, store the original plus several scaled sizes."""
    base_image = os.path.join(BASE_DIR, "logo-base.png")
    base_image_small = os.path.join(BASE_DIR, "logo-base-small.png")
    with open(base_image, "rb") as image_flo:
        with open(base_image_small, "rb") as image_flo_small:
            # Scale the image to various widths and store them
            for filename, width in SQUARE_SIZES.items():
                extension = os.path.splitext(filename)[0]
                fmt = FORMAT_MAP.get(extension, "PNG")

                if width > 32:
                    scaled_flo = image.scale_flo(image_flo, width, fmt=fmt)
                else:
                    scaled_flo = image.scale_flo(image_flo_small, width, fmt=fmt)
                out_path = os.path.join(BASE_DIR, filename)
                with open(out_path, "wb") as fs:
                    fs.truncate()
                    scaled_flo.seek(0)
                    shutil.copyfileobj(scaled_flo, fs)
                    print(f"Wrote {out_path}")


def main():
    """Wrap and run the generate_images function."""
    try:
        generate_images()
    except KeyboardInterrupt:
        # Write a nice message to stderr
        sys.stderr.write("\n\033[91m\u2717 Operation canceled by user.\033[0m\n")
        sys.exit(errno.EINTR)


if __name__ == "__main__":
    main()
