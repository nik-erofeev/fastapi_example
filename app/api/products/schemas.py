from pydantic import BaseModel


class ProductBaseSchemas(BaseModel):
    name: str
    description: str
    price: int


class ProductCreateSchemas(ProductBaseSchemas):
    pass


class ProductUpdateSchemas(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class ProductResponseSchemas(ProductBaseSchemas):
    id: int

    class Config:
        from_attributes = True
