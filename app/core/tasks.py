import json
from django.db.utils import IntegrityError

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from celery import shared_task
from django_app.models import ProviderModel, CurrencyModel, BlockModel
from fastapi_app.schema.block import BlokSchema, ProviderSchema, CurrencySchema
import logging

# Initialize logger
logger = logging.getLogger(__name__)


def get_block(provider: ProviderSchema, currency: CurrencySchema) -> BlokSchema | None:
    """
    Fetches the latest block data from the blockchain service.

    Args:
        provider (ProviderSchema): The provider model with service details.
        currency (CurrencySchema): The currency model for which the block data is requested.

    Returns:
        BlokSchema | None: Returns block data if successful, otherwise None.

    Logs:
        - Errors for connection issues and missing block data.
    """
    # Request setup
    url = str(provider.link).format(currency=currency.name)
    headers = {"Accepts": "application/json"}
    if provider.api_key:
        headers.update({"X-CMC_PRO_API_KEY": provider.api_key})

    session = Session()
    session.headers.update(headers)

    try:
        # Send request to blockchain service
        response = session.get(url)
        if response.status_code != 200:
            logger.error("Cant connect to blockchain service")
            return

        # Parse response and create block schema
        data = json.loads(response.text).get("data")
        last_block = data[0] if isinstance(data, list) else next(iter(data.values()))
        block_id = last_block.get("id")
        if not block_id:
            logger.exception("Block ID not found")
            return

        return BlokSchema(
            number=block_id,
            created_at=last_block.get("first_block_timestamp") or last_block.get("time"),
            fk_to_currency=currency,
            provider=provider,
        )

    except (ConnectionError, Timeout, TooManyRedirects):
        logger.error("Cant connect to blockchain service")


@shared_task
def load_data():
    """
    Periodically loads block data from blockchain services for all providers and currencies.

    Fetches the latest block for each currency and provider and stores it in the database.

    Logs the update of each provider.
    """
    providers = ProviderModel.objects.all()
    currencies = CurrencyModel.objects.all()

    for provider in providers:
        p = ProviderSchema.model_validate(provider)
        for currency in currencies:
            c = CurrencySchema.model_validate(currency)
            block = get_block(p, c)
            if block:
                db_block = BlockModel(
                    fk_to_currency=currency,
                    provider=provider,
                    **block.model_dump(exclude=("fk_to_currency", "provider")),
                )
                try:
                    db_block.save()
                except IntegrityError:
                    pass
        logger.info(f"provider {provider} updated")
