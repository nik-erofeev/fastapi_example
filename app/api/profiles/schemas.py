from pydantic import BaseModel


class ProfileBaseSchemas(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


class ProfileCreateSchemas(ProfileBaseSchemas):
    pass


class ProfileUpdateSchemas(ProfileBaseSchemas):
    pass


class ProfileResponseSchemas(ProfileBaseSchemas):
    user_id: int
    id: int

    class Config:
        from_attributes = True
