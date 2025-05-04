from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(500), nullable=False)
    rating = Column(Integer(), CheckConstraint('rating >= 0 AND rating <= 5'), nullable=False)
    item_id = Column(Integer(), ForeignKey('menu.id'), nullable=False)

    menu = relationship('Menu', back_populates='review')
