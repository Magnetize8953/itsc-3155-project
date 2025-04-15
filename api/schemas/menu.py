from typing import Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str
    cost: float
    calories: int
    category: str
    resources: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    cost: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None
    resources: Optional[str] = None


class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True
