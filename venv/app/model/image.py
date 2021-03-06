from __future__ import annotations
from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.model.product import Product


class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String)

    product_id = Column(Integer, ForeignKey('products.product_id'))

    product: Product = relationship('Product', back_populates='more_image')