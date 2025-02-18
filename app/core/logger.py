from config import settings

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": settings.loglevel,
            "class": "logging.FileHandler",
            "filename": "/app/logs/django.log",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {name} {message} {asctime}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": settings.loglevel,
            "propagate": True,
        },
        "celery": {
            "handlers": ["file", "console"],
            "level": settings.loglevel,
            "propagate": True,
        },
    },
}
