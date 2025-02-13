from uuid import UUID

from pydantic import Field, field_validator, model_validator

from jwt_auth.utils import hash_password, validate_password
from schemas.schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    username: str = Field(min_length=4, max_length=24, pattern=r'^[a-zA-Z0-9-_]*$')
    email: str | None = None
    is_active: bool = True


class CreateUserSchema(UserBaseSchema):
    password1: str | bytes = Field(min_length=8)
    password2: str | bytes = Field(min_length=8)

    @field_validator('password1', )
    def password_validation(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(c.isalpha() for c in value):
            raise ValueError("Password must contain at least one letter")

        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number")

        if not any(c in "!@#$%^&()_+-={}[]\|:;'<>,.?/" for c in value):
            raise ValueError("Password must contain at least one special character")

        return hash_password(value)

    @model_validator(mode='after')
    def passwords_match(self):
        if not validate_password(self.password2, self.password1):
            raise ValueError("passwords do not match")
        return self


class BrowseUserSchema(BaseSchema):
    username: str


class ReadUserSchema(UserBaseSchema):
    uuid: UUID


class LoginUserSchema(UserBaseSchema):
    password: str


class UpdateUserSchema(BaseSchema):
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None
