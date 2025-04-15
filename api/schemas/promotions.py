from datetime import datetime
from pydantic import BaseModel


class PromotionBase(BaseModel):
    code: str
    expire_date: datetime
    item_id: int


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True
