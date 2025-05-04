from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    # mysql doesn't let you do date_add for defaults
    # time is just an integer that gets parsed. time + 1000000 is right now tomorrow
    expire_date = Column(DATETIME, server_default=func.now() + 1000000)
    discount = Column(Integer, nullable=False)

