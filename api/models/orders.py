from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DATETIME, server_default=str(datetime.now()))
    status = Column(String(20))
    total = Column(DECIMAL(10, 2), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    # WARNING: validation must happen on server before committing to db
    items = Column(String(200), nullable=False)
    promo = Column(String(100), nullable=True)

    customer = relationship('Customer', back_populates='order')
