from logging.config import dictConfig

LOG_CONFIG: dict[str, object] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[%(levelname)s] %(message)s  [%(name)s:%(lineno)s]"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "tests": {"handlers": ["console"], "level": "DEBUG"},
        "emerald_heart": {"handlers": ["console"], "level": "INFO"},
        "boltons": {"handlers": ["console"], "level": "WARNING"},
        "django": {"handlers": ["console"], "level": "WARNING"},
    },
}
dictConfig(LOG_CONFIG)
