from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone_number = Column(String(40), unique=True, nullable=True)
    address = Column(String(100), nullable=True)
    hours_worked = Column(Integer, nullable=True)