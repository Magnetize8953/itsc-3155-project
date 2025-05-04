from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone_number = Column(String(40), unique=True, nullable=True)
    address = Column(String(100), nullable=True)
    payment_info = Column(Integer(), ForeignKey('payments.id'))

    payment = relationship('Payment', back_populates='customer')
    order = relationship('Order', back_populates='customer')
