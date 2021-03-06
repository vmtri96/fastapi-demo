from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import sqlalchemy as db
from app.base import Base
from typing import List, TYPE_CHECKING

from app.dto.role_dto import RoleDtoIn


if TYPE_CHECKING:
    from app.model.user import User


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    users: List[User] = relationship("User", back_populates="role")

