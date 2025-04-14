from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    card_info: str
    status: str
    type: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    card_info: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True
