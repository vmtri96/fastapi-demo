from __future__ import annotations
from app.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from app.model.status import Status
    from app.model.user import User
    from app.model.coupon import Coupon
    from app.model.product import Product


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    shipping_address = Column(String)
    shipping_fee = Column(Integer)
    total_price = Column(Integer)
    created_date = Column(DateTime)

    user_id = Column(Integer, ForeignKey('users.user_id'))
    status_id = Column(Integer, ForeignKey('status.status_id'))
    coupon_id = Column(Integer, ForeignKey('coupon.coupon_id'))

    user: User = relationship('User', back_populates='orders')
    status: Status = relationship('Status', back_populates='orders')
    coupon: Coupon = relationship('Coupon', back_populates='orders')
    products: List[Product] = relationship('Product', secondary='order_product', back_populates='orders')