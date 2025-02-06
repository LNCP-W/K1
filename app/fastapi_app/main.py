import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()

from fastapi import FastAPI
from asgiref.sync import sync_to_async
from django_app.models import User


app = FastAPI()

async def get_user():
    users = await sync_to_async(lambda: list(User.objects.all()))()
    return users

@app.get("/items/")
async def read_items():
    items = await get_user()
    return items
