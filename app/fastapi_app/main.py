import os
from pathlib import Path
from config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import logging
from fastapi import FastAPI
from fastapi_app.routers import block_router, user_router, security_router


def get_fastapi() -> FastAPI:
    """FastAPI initialization"""

    # Create logger
    logger = logging.getLogger("fastapi")
    logger.setLevel(settings.loglevel)
    file_handler = logging.FileHandler("/app/logs/fastapi.log")
    file_handler.setLevel(settings.loglevel)
    formatter = logging.Formatter("%(levelname)s %(name)s %(message)s %(asctime)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create app
    app = FastAPI()

    # Add routers
    app.include_router(block_router)
    app.include_router(user_router)
    app.include_router(security_router)
    # Folder creation
    Path("static").mkdir(parents=True, exist_ok=True)
    Path("media").mkdir(parents=True, exist_ok=True)

    return app
