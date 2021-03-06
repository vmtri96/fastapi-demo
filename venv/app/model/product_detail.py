from __future__ import annotations
from app.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.model.product import Product


class ProductDetail(Base):
    __tablename__ = 'product_detail'

    pdetail_id = Column(Integer, primary_key=True, autoincrement=True)
    more_description = Column(String)

    product_id = Column(Integer, ForeignKey('products.product_id'))

    product: Product = relationship('Product', back_populates='product_detail')

