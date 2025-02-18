from django.db.models import Q, Max
from datetime import datetime, timezone
from django_app.models import UserModel, ProviderModel, BlockModel
from django.core.paginator import Paginator

from asgiref.sync import sync_to_async
from fastapi_app.schema.user import UserSchema
from fastapi_app.schema.block import ProviderSchema, BlokSchema
from time import time


class DB:
    """
    A class to interact with the database asynchronously. It provides methods for
    user and block retrieval, creation, and pagination, as well as querying
    providers.
    """

    @sync_to_async
    def get_user(
        self,
        user_id: int | None = None,
        email: str | None = None,
        username: str | None = None,
    ) -> UserSchema:
        """
        Fetches a user from the database based on provided filters. Filters can include
        user_id, email, or username. Returns a validated user schema or None if not found.

        Args:
            user_id (int, optional): The user ID.
            email (str, optional): The email address.
            username (str, optional): The username.

        Returns:
            UserSchema: The validated user schema or None if not found.
        """
        filters = {}
        if user_id:
            filters["id"] = user_id
        if email:
            filters["email"] = email
        if username:
            filters["username"] = username
        db_user = UserModel.objects.filter(**filters).first()
        return UserSchema.model_validate(db_user) if db_user else None

    @sync_to_async
    def get_users(self) -> list[UserSchema]:
        """
        Fetches all users from the database and returns a list of validated user schemas.

        Returns:
            list[UserSchema]: A list of validated user schemas.
        """
        db_users = UserModel.objects.all()
        return [UserSchema.model_validate(user) for user in db_users]

    @sync_to_async
    def create_user(self, user: UserSchema) -> UserSchema:
        """
        Creates a new user in the database and returns the validated user schema.

        Args:
            user (UserSchema): The user schema to be created.

        Returns:
            UserSchema: The validated schema of the newly created user.
        """
        db_user = UserModel(**user.model_dump())
        db_user.save()
        new_user = UserSchema.model_validate(db_user)
        new_user.updated_at = datetime.now(timezone.utc)
        return new_user

    @sync_to_async
    def get_providers(self) -> list[ProviderSchema]:
        """
        Fetches all providers from the database and returns a list of validated provider schemas.

        Returns:
            list[ProviderSchema]: A list of validated provider schemas.
        """
        db_providers = ProviderModel.objects.all()
        return [ProviderSchema.model_validate(user) for user in db_providers]

    @sync_to_async
    def get_blocks(
        self,
        currency: str | None = None,
        provider: int | None = None,
        page: int = 1,
        per_page: int = 20,
        cursor: int | None = None,
    ) -> list[BlokSchema]:
        """
        Fetches blocks from the database with pagination and optional filtering by currency,
        provider, and cursor.

        Args:
            currency (str, optional): The currency to filter by.
            provider (int, optional): The provider ID to filter by.
            page (int, optional): The page number for pagination (default is 1).
            per_page (int, optional): The number of results per page (default is 20).
            cursor (int, optional): The cursor for pagination, filtering results by ID.

        Returns:
            list[BlokSchema]: A list of validated block schemas.
        """
        t1 = time()
        filters = Q()
        if currency is not None:
            filters &= Q(fk_to_currency__name=currency)
        if cursor is not None:
            filters &= Q(id__lte=cursor)
        if provider is not None:
            filters &= Q(provider=provider)

        db_blocks = (
            BlockModel.objects.select_related("fk_to_currency")
            .filter(filters)
            .order_by("-id")
        )
        paginator = Paginator(db_blocks, per_page)
        page_data = paginator.page(page)
        blocks = [BlokSchema.model_validate(i) for i in list(page_data)]
        print(time() - t1)
        return blocks

    @sync_to_async
    def get_max_block_ind(self):
        """
        Fetches the maximum block ID from the database.

        Returns:
            int: The maximum block ID.
        """
        cursor = BlockModel.objects.aggregate(max_id=Max("id"))["max_id"]
        print(cursor)
        return cursor

    @sync_to_async
    def get_block(
        self,
        block_id: int | None,
        currency: str | None = None,
        number: int | None = None,
    ) -> BlokSchema:
        """
        Fetches a specific block from the database by its ID, currency, and number.

        Args:
            block_id (int, optional): The block ID.
            currency (str, optional): The currency to filter by.
            number (int, optional): The block number to filter by.

        Returns:
            BlokSchema: The validated block schema or None if not found.
        """
        filters = Q()
        if block_id is not None:
            filters &= Q(id=block_id)
        else:
            filters &= Q(fk_to_currency__name=currency)
            filters &= Q(number=number)
        db_user = (
            BlockModel.objects.select_related("fk_to_currency").filter(filters).first()
        )
        if db_user:
            return BlokSchema.model_validate(db_user)
