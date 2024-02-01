from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 50
