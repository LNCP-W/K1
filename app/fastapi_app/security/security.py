from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from fastapi_app.schema.user import UserSchema
from fastapi_app.schema.token import TokenDataSchema
from fastapi_app.db import DB
from fastapi_app.security.exeptions import credentials_exception, login_exception
from fastapi_app.security.utils import verify_password
from config import settings
from datetime import timedelta, datetime, timezone

# OAuth2 password bearer token schema.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")


def decode_token(token: str) -> TokenDataSchema | None:
    """
    Decodes the provided JWT token and returns the decoded payload as a TokenDataSchema object.

    This function verifies the JWT token using the secret and algorithm specified in the configuration.
    It extracts the 'sub' field (username) and returns a TokenDataSchema instance.
    If the token is invalid or the username is not found, it raises a credentials_exception.

    Args:
        token (str): The JWT token to be decoded.

    Returns:
        TokenDataSchema | None: Decoded token data or None if decoding fails.

    Raises:
        credentials_exception: If the token is invalid or the 'sub' field is not present.
    """
    try:
        # Decode the token
        payload = jwt.decode(
            token,
            settings.security.jwt_secret,
            algorithms=[settings.security.jwt_algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Return TokenDataSchema with the username
        token_data = TokenDataSchema(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


async def auth_user(username: str, password: str, db:DB) -> UserSchema:
    """
    Authenticates a user by checking if the provided username and password match the database record.

    This function retrieves the user from the database based on the username and then verifies the password
    using the 'verify_password' utility function. If the user does not exist or the password is incorrect,
    a login_exception is raised.

    Args:
        username (str): The username of the user to be authenticated.
        password (str): The password to be checked.
        db (DB): The database object to use to authenticate the user.

    Returns:
        UserSchema: The authenticated user schema if the authentication is successful.

    Raises:
        login_exception: If the username does not exist or the password is incorrect.
    """
    user = await db.get_user(username=username)
    if not user or not verify_password(password, user.password):
        raise login_exception
    # Set the password to None for security reasons before returning the user
    user.password = None
    return user


def create_token(data: dict) -> str:
    """
    Creates a JWT token for the user with the provided data.

    This function generates a JWT token that includes the given data and adds an expiration time
    based on the configuration. The token is encoded using the JWT secret and algorithm specified
    in the configuration.

    Args:
        data (dict): A dictionary containing the user data (e.g., username) to be encoded into the token.

    Returns:
        str: The generated JWT token.
    """
    token_expire_minutes = timedelta(minutes=settings.security.token_expire_minutes)
    data_copy = data.copy()
    # Set the expiration time for the token
    expire = datetime.now(timezone.utc) + token_expire_minutes
    data_copy.update({"exp": expire})
    # Encode the token
    token = jwt.encode(
        data_copy,
        settings.security.jwt_secret,
        algorithm=settings.security.jwt_algorithm,
    )
    return token
