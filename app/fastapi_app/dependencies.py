from fastapi_app.db import DB
from fastapi import Depends
from fastapi_app.schema.user import UserSchema
from fastapi_app.security.exeptions import credentials_exception
from fastapi_app.security.security import oauth2_scheme, decode_token


async def get_db() -> DB:
    _db = DB()
    return _db


async def get_current_user(token: str = Depends(oauth2_scheme), db: DB = Depends(get_db)) -> UserSchema:
    token_data = decode_token(token)
    user = await db.get_user(username=str(token_data.username))
    if not user:
        raise credentials_exception
    user.password = None
    return user
