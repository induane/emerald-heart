from __future__ import annotations

from .base import *  # noqa

DEBUG = True

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": BASE_DIR.joinpath(".db.sqlite3"),
    }
}
