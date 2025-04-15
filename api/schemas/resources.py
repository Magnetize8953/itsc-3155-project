from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    name: str
    amount: int
    unit: str


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[int] = None


class Resource(ResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True
