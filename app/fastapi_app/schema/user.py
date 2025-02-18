from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from datetime import datetime, timezone
from fastapi_app.security.utils import hash_password


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "new_user",
                "email": "new_user@example.com",
                "password": "strong_password123",
                "is_active": True,
                "is_superuser": False,
                "is_staff": False,
            }
        }



class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128,
                          examples=["StrongPass123!",])

    @field_validator('password')
    def check_password_strength(cls, password):
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit.')

        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character.')

        return password


    class Config:
        json_schema_extra = {
            "example": {
                "username": "new_user",
                "email": "new_user@example.com",
                "password": "strong_password123",
            }
        }



class UserSchema(UserBaseSchema):
    password: str
    updated_at: datetime | None = None
    date_joined: datetime  = Field(default_factory=lambda :datetime.now(timezone.utc))

    def hash_password(self) -> None:
        # Hash password before save in DB
        self.password = hash_password(self.password)



class UserOutSchema(UserBaseSchema):
    pass
