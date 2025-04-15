from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')
    unit = Column(String(20), nullable=False)
