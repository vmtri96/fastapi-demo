from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base
from typing import TYPE_CHECKING, List


class OrderProduct(Base):
    __tablename__ = 'order_product'
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Integer)

