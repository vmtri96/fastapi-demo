from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.base import Base
from typing import List, TYPE_CHECKING
import sqlalchemy as db

from app.dto.product_type_dto import ProductTypeDtoIn


if TYPE_CHECKING:
    from app.model.product import Product


class ProductType(Base):
    __tablename__ = 'product_type'

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    products: List[Product] = relationship("Product", back_populates="type")


    @staticmethod
    def create_product_type(session: db.orm.Session, product_type_dto: ProductTypeDtoIn):
        product_type = ProductType(name=product_type_dto.name)
        session.add(product_type)
        session.commit()
        return product_type_dto
