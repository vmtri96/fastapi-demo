from __future__ import annotations
from app.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from app.model.order import Order


class Coupon(Base):
    __tablename__ = 'coupon'

    coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    code = Column(String)
    quantity = Column(Integer)
    discount = Column(Float)
    apply_for = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    orders: List[Order] = relationship('Order', back_populates='coupon')