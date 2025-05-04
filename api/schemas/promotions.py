from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    code: str
    expire_date: Optional[datetime] = None
    discount: int


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True
