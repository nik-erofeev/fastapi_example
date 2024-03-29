import enum

from pydantic import BaseModel, constr, EmailStr


class BaseResponseModel(BaseModel):
    """класс выходящего из БД"""

    class Config:
        from_attributes = True


class UserBaseSchemas(BaseModel):
    email: EmailStr
    username: str


class UserCreateSchemas(UserBaseSchemas):
    password: str


class UserResponseSchemas(UserBaseSchemas, BaseResponseModel):
    roles: enum.StrEnum
    id: int


class UserDeleteResponseSchemas(UserBaseSchemas, BaseResponseModel):
    id: int
    is_deleted: bool


class UserUpdateSchemas(BaseModel):
    email: EmailStr | None = None
    username: str | None = None


class UserQueryParams(BaseModel):
    email: EmailStr | None = None
    username: str | None = None


class UserChangePasswordRequest(BaseModel):
    new_password: constr(max_length=256)


class UserByUsernameRequest(BaseModel):
    username: str


class UpdatedUserResponseRoles(BaseModel):
    updated_user_id: int


class UserResponseTest(BaseModel):
    roles: enum.StrEnum
