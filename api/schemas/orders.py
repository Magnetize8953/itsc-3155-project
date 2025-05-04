from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    date: datetime
    status: str
    total: float
    customer_id: int
    items: str
    promo: str


class OrderCreate(BaseModel):
    status: str
    customer_id: int
    items: str
    promo: str


class OrderUpdate(BaseModel):
    status: Optional[str] = None

class Order(OrderBase):
    id: int

    class ConfigDict:
        from_attributes = True
