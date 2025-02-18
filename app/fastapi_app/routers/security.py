from fastapi import APIRouter
from fastapi import Depends, Request, HTTPException
from fastapi_app.schema.token import TokenSchema
from fastapi_app.security.security import auth_user, create_token
from fastapi_app.dependencies import DB, get_db
from fastapi.security import OAuth2PasswordRequestForm


security_router = APIRouter(
    prefix="/security",  # Prefix for all routes in this router
    tags=["security"],  # Tag to categorize the routes
    dependencies=[],  # No global dependencies for this router
    responses={404: {"description": "Not found"}},  # Default response for 404 errors
)


@security_router.post(
    "/token",
    response_model=TokenSchema,  # The response model that will be returned
    tags=["login"],  # Tags to categorize the route as related to log
    description="Use only username and password to obtain an access token",  # Detailed description of the route
)
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db:DB = Depends(get_db)
):
    """
    Endpoint to authenticate the user and return an access token.

    This endpoint takes the username and password from the request body and validates the credentials.
    If valid, it returns an access token which can be used for further API requests.

    Parameters:
        - form_data (OAuth2PasswordRequestForm): A FastAPI form that requires `username` and `password` fields.

    Raises:
        HTTPException:
            - 401 if the credentials are invalid.

    Returns:
        TokenSchema: Contains the `access_token` and `token_type` (bearer).
    """
    # Authenticate the user using the provided username and password
    user = await auth_user(form_data.username.lower(), form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token for the authenticated user
    access_token = create_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
