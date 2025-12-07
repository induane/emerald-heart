from __future__ import annotations

import os
import tempfile
from pathlib import Path

from .base import *  # noqa

TEMP_DIR = Path(tempfile.gettempdir()).joinpath("emerald-test")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Setup the test database
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": TEMP_DIR.joinpath("emerald-test-db.sqlite"),
    }
}

# Increase the range of ports the Django LiveServerTestCase can spawn on
os.environ["DJANGO_LIVE_TEST_SERVER_ADDRESS"] = "localhost:8082-9092"
