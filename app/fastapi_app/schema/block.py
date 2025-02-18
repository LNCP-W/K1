from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime, timezone


class CurrencySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "bitcoin",
            }
        }


class ProviderBaseSchema(BaseModel):
    id: int|None = None
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "coinmarketcap",
            }
        }


class ProviderSchema(ProviderBaseSchema):
    api_key: str | None = None
    link: HttpUrl

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "coinmarketcap",
                "link": "https://sandbox-api.coinmarketcap.com/v1/blockchain/statistics/latest?slug={currency}",
                "api_key": "<KEY>",

            }
        }


class ProviderOutSchema(ProviderBaseSchema):
    pass


class BlokBaseSchema(BaseModel):
    id: int | None = None
    fk_to_currency: CurrencySchema
    number: int
    created_at: datetime | None = None
    stored_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provider: ProviderSchema

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "fk_to_currency":
                    {
                        "id": 1,
                        "name": "bitcoin"
                    },
                'created_at': "2025-02-18T01:56:41.689604+00:00",
                'stored_at': "2025-02-18T01:56:41.689604+00:00",
                'provider': {                "id": 1,
                "name": "coinmarketcap",
                "link": "https://sandbox-api.coinmarketcap.com/v1/blockchain/statistics/latest?slug={currency}",
                "api_key": "<KEY>",
}


            }
        }


class BlokOutSchema(BlokBaseSchema):
    provider: ProviderOutSchema

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "fk_to_currency":
                    {
                        "id": 1,
                        "name": "bitcoin"
                    },
                'created_at': "2025-02-18T01:56:41.689604+00:00",
                'stored_at': "2025-02-18T01:56:41.689604+00:00",
                'provider': {"id": 1,
                             "name": "coinmarketcap",
                             }

            }
        }


class BlokSchema(BlokBaseSchema):
    pass
