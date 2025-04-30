from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    calories = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
    # WARNING: validation must happen on server before committing to db
    resources = Column(String(500), nullable=False)
