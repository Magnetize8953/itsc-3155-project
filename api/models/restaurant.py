from sqlalchemy import Column, Integer, DECIMAL, DATE
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total = Column(DECIMAL(10, 2), default=0.0)
    op_date = Column(DATE, server_default=func.now())
    orders = Column(Integer, default=0)
