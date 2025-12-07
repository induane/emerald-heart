"""Logging Configuration."""

from __future__ import annotations

import os

PROD_LOGGING: bool = "production" in (os.environ.get("DJANGO_SETTINGS_MODULE", ""), None)
LOG_LEVEL: str = "INFO" if PROD_LOGGING else "DEBUG"

# Logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "%(levelname)8s -- %(message)s %(name)s:%(lineno)s",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.contrib.staticfiles": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "emerald_heart": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "emerald_heart.core": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
}
