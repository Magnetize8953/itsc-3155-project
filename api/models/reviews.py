from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(500), nullable=False)
    rating = Column(Integer(), CheckConstraint('rating >= 0 AND rating <= 5'), unique=True, nullable=False)
    customer_id = Column(Integer(), ForeignKey('customers.id'), nullable=False)

    customer = relationship('Customer', back_populates='review')
