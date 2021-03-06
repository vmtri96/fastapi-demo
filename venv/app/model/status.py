from __future__ import annotations
from app.base import Base
import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.model.user import User
    from app.model.order import Order


class Status(Base):
    __tablename__ = 'status'

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    users: List[User] = relationship("User", back_populates="status")
    orders: List[Order] = relationship('Order', back_populates='status')