from sqlalchemy import Column, Integer, String, DATETIME
from datetime import datetime, timedelta
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    expire_date = Column(DATETIME, server_default=str(datetime.now() + timedelta(days=1)))
    discount = Column(Integer, nullable=False)

