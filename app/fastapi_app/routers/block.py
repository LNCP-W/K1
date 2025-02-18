from fastapi import APIRouter, HTTPException, Depends, Query

from fastapi_app.schema.block import (
    BlokOutSchema,
    ProviderOutSchema,
)
from fastapi_app.db import DB
from fastapi_app.dependencies import get_db, get_current_user


block_router = APIRouter(
    prefix="/block",  # Prefix for all routes in this router
    tags=["block"],  # Tag to categorize the routes
    dependencies=[Depends(get_current_user)],  # Dependency to check the current user
    responses={404: {"description": "Not found"}},  # Default response for 404 errors
)


@block_router.get("/providers/", response_model=list[ProviderOutSchema])
async def get_providers(db: DB = Depends(get_db)):
    """
    Endpoint to retrieve the list of providers.

    This endpoint fetches all the providers from the database.

    Parameters:
        - db (DB): Database dependency to interact with the database.

    Returns:
        List[ProviderOutSchema]: List of providers.
    """
    return await db.get_providers()


@block_router.get("/list", response_model=list[BlokOutSchema])
async def get_blocks(
    currency: str | None = None,
    provider_id: int | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: DB = Depends(get_db),
):
    """
    Endpoint to retrieve a list of blocks with pagination.

    This endpoint returns a paginated list of blocks, optionally filtered by `currency` and `provider_id`.

    Parameters:
        - currency (str | None): Optional filter by currency.
        - provider_id (int | None): Optional filter by provider ID.
        - page (int): Page number for pagination, defaults to 1.
        - per_page (int): Number of items per page, defaults to 20 (max 100).
        - db (DB): Database dependency to interact with the database.

    Returns:
        List[BlokOutSchema]: List of blocks.
    """
    blocks = await db.get_blocks(currency, provider_id, page, per_page)
    return [BlokOutSchema.model_validate(i) for i in blocks]


@block_router.get("/fast_list/", response_model=list[BlokOutSchema])
async def get_blocks_fast(
    currency: str | None = None,
    cursor: int = Query(None, ge=0),
    per_page: int = Query(20, ge=1, le=100),
    db: DB = Depends(get_db),
):
    """
    Fast endpoint to retrieve a list of blocks based on a cursor.

    This endpoint is optimized for faster fetching of blocks with a cursor-based pagination mechanism.

    Parameters:
        - currency (str | None): Optional filter by currency.
        - cursor (int | None): Cursor for pagination, used to fetch subsequent blocks.
        - per_page (int): Number of items per page, defaults to 20 (max 100).
        - db (DB): Database dependency to interact with the database.

    Returns:
        List[BlokOutSchema]: List of blocks.
    """
    if cursor is None:
        cursor = await db.get_max_block_ind()

    blocks = await db.get_blocks(currency, per_page=per_page, cursor=cursor)
    return [BlokOutSchema.model_validate(i) for i in blocks]


@block_router.get("/", response_model=BlokOutSchema)
async def get_block(
    block_id: int | None = None,
    currency: str | None = None,
    number: int | None = None,
    db: DB = Depends(get_db),
):
    """
    Endpoint to retrieve a specific block by its `block_id`, `currency`, and `number`.

    This endpoint either fetches a block by its ID or by the combination of currency and block number.

    Parameters:
        - block_id (int | None): Optional filter by block ID.
        - currency (str | None): Optional filter by currency.
        - number (int | None): Optional filter by block number.
        - db (DB): Database dependency to interact with the database.

    Raises:
        HTTPException:
            - 400 if both `block_id` and combination of `currency` & `number` are provided.
            - 404 if the block is not found.

    Returns:
        BlokOutSchema: The block details.
    """
    if (block_id is None and (currency is None or number is None)) or (
        block_id is not None and (currency is not None or number is not None)
    ):
        raise HTTPException(
            status_code=400,
            detail="Provide only block_id or combination of currency and number",
        )
    block = await db.get_block(block_id, currency, number)
    if block is None:
        raise HTTPException(status_code=404, detail="Not found")
    return BlokOutSchema.model_validate(block)
