from typing import Optional
from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
    hours_worked: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    hours_worked: Optional[int] = None


class Employee(EmployeeBase):
    id: int

    class ConfigDict:
        from_attributes = True
