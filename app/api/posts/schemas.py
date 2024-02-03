from pydantic import BaseModel


class PostBaseSchemas(BaseModel):
    title: str
    body: str


class PostCreateSchemas(PostBaseSchemas):
    pass


class PostUpdateSchemas(BaseModel):
    title: str | None = None
    body: str | None = None


class PostResponseSchemas(PostBaseSchemas):
    user_id: int
    id: int

    class Config:
        from_attributes = True
