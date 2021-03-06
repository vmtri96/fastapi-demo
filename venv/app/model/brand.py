from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.base import Base
from typing import List, TYPE_CHECKING
import sqlalchemy as db


if TYPE_CHECKING:
    from app.model.product import Product


class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country = Column(String)

    products: List[Product] = relationship('Product', back_populates='brand')

