from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    expire_date = Column(DATETIME, server_default=str(datetime.now() + timedelta(days=1)))
    item_id = Column(Integer, ForeignKey('menu.id'), nullable=False)

    menu_item = relationship('Menu', back_populates='promotion')
