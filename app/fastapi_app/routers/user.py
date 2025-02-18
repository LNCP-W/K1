from fastapi import APIRouter, Depends, HTTPException

from django_app.models import UserModel
from fastapi_app.schema.user import UserSchema, UserOutSchema, UserCreateSchema
from fastapi_app.db import DB
from fastapi_app.dependencies import get_db, get_current_user


user_router = APIRouter(
    prefix="/user",  # Prefix for all routes in this router
    tags=["user"],  # Tag to categorize the routes
    responses={404: {"description": "Not found"}},  # Default response for 404 errors
)


@user_router.get("/me/", response_model=UserOutSchema)
async def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    """
    Endpoint to get the current authenticated user's information.

    This endpoint returns the information about the authenticated user such as `username`, `email`, and other details.

    Parameters:
        - current_user (UserModel): The currently authenticated user, injected by `get_current_user` dependency.

    Returns:
        UserOutSchema: The current user's information.
    """
    return UserOutSchema.model_validate(current_user)


@user_router.post("/create/", response_model=UserOutSchema)
async def create_user(user: UserCreateSchema, db: DB = Depends(get_db)):
    """
    Endpoint to create a new user.

    This endpoint takes the necessary fields to create a new user and ensures that the username is unique before creating the user.
    If the username already exists, it will raise a `400` error.

    Parameters:
        - user (UserCreateSchema): The schema containing the `username`, `email`, and `password` to create the new user.
        - db (DB): Database dependency to interact with the user database.

    Raises:
        HTTPException:
            - 400 if the username already exists.

    Returns:
        UserOutSchema: The created user's information.
    """
    new_user = UserSchema.model_validate(user)
    existing_user = await db.get_user(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user.hash_password()  # Hash the user's password before saving
    new_user = await db.create_user(new_user)  # Save the user to the database
    return UserOutSchema.model_validate(new_user)  # Return the created user info
