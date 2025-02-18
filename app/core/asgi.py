"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application


"""
Settings
"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


"""
Django settings
"""
django_app = get_asgi_application()

from fastapi_app.main import get_fastapi
from fastapi.staticfiles import StaticFiles

fastapi_app = get_fastapi()


fastapi_app.mount("/django", django_app)
fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
fastapi_app.mount("/media", StaticFiles(directory="media"), name="media")
