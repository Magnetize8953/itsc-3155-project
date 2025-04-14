from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_info = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)

    customer = relationship('Customer', back_populates='payment')
