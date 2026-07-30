from __future__ import annotations

import os

from .base import *  # noqa

get_env = os.environ.get

UPLOAD_SERVE_FOLDER = Path("/emerald_heart/volume/uploads/")
UPLOAD_SERVE_FOLDER.parent.mkdir(parents=True, exist_ok=True)
UPLOAD_TEMP_FOLDER = Path("/emerald_heart/volume/upload_temp/")
UPLOAD_TEMP_FOLDER.parent.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = Path("/emerald_heart/volume/db/database.db.sqlite3")
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
STATIC_ROOT = Path("/emerald_heart/static/")
STATIC_URL: str = "/s/emerald-heart/"


CSRF_TRUSTED_ORIGINS = [
    "https://emerald-directory.fly.dev/",
    "https://*.fly.dev",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_PATH,
        "OPTIONS": {
            "init_command": (
                "PRAGMA foreign_keys=ON;"
                "PRAGMA journal_mode = WAL;"
                "PRAGMA synchronous = NORMAL;"
                "PRAGMA busy_timeout = 5000;"
                "PRAGMA temp_store = MEMORY;"
                "PRAGMA mmap_size = 134217728;"
                "PRAGMA journal_size_limit = 67108864;"
                "PRAGMA cache_size = 2000;"
            ),
            "transaction_mode": "EXCLUSIVE",
        },
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": "/emerald_heart/volume/query_cache/",
        "MAX_ENTRIES": 10_000,
        "TIMEOUT": None,
        "SHARDS": 8,
        "DATABASE_TIMEOUT": 1.0,
        "OPTIONS": {"size_limit": 4_294_967_296},  # 4 gigabytes ( 2**32 )
    }
}

# Enable manifest staticfiles
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "emerald-directory.fly.dev",
    "localhost",
    "fly.dev",
]

FLY_APP_NAME = os.getenv("FLY_APP_NAME")
if FLY_APP_NAME:
    ALLOWED_HOSTS.append(f"{FLY_APP_NAME}.fly.dev")

SECRET_KEY = get_env("SECRET_KEY")
SITE_ID = get_env("SITE_ID")
