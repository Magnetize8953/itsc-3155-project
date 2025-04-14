from typing import Optional
from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    payment_info: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True
