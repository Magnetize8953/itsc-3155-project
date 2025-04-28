from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RestaurantBase(BaseModel):
    total: float
    orders: int


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    total: Optional[float] = None
    orders: Optional[int] = None


class Restaurant(RestaurantBase):
    id: int
    op_date: datetime

    class ConfigDict:
        from_attributes = True
