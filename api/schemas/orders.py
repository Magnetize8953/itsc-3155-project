from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    date: datetime
    status: str
    total: float
    customer_id: int
    items: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    date: Optional[datetime] = None
    status: Optional[str] = None
    total: Optional[float] = None
    customer_id: Optional[int] = None
    items: Optional[str] = None


class Order(OrderBase):
    id: int

    class ConfigDict:
        from_attributes = True
