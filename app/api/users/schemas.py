from pydantic import BaseModel, constr, EmailStr


class BaseResponseModel(BaseModel):
    """класс выходящего из БД"""

    class Config:
        from_attributes = True


class UserBaseSchemas(BaseModel):
    email: EmailStr


class UserCreateSchemas(UserBaseSchemas):
    password: str


class UserResponseSchemas(UserBaseSchemas, BaseResponseModel):
    id: int


class UserUpdateSchemas(BaseModel):
    email: EmailStr | None = None


class UserChangePasswordRequest(BaseModel):
    new_password: constr(max_length=256)
