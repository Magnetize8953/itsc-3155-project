from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    text: str
    rating: int
    item_id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    text: str
    rating: int


class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True
