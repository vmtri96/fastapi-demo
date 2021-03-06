from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy
from app.base import Base
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from app.model.role import Role
    from app.model.product import Product
    from app.model.status import Status
    from app.model.order import Order


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

    role_id = Column(Integer, ForeignKey('roles.role_id'))
    status_id = Column(Integer, ForeignKey('status.status_id'))

    role: Role = relationship("Role", back_populates="users")
    status: Status = relationship("Status", back_populates="users")
    orders: List[Order] = relationship('Order', back_populates='user')
    products: List[Product] = relationship('Product', back_populates='user')


    def __repr__(self):
        return f"<User id={self.user_id}, username={self.username}, name={self.name}, role={self.role}"
