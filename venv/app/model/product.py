from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.base import Base
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from app.model.product_type import ProductType
    from app.model.brand import Brand
    from app.model.product_detail import ProductDetail
    from app.model.image import Image
    from app.model.order import Order
    from app.model.user import User


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    image = Column(String)
    quantity = Column(Integer)
    import_date = Column(DateTime)
    import_price = Column(Integer)

    type_id = Column(Integer, ForeignKey('product_type.type_id'))
    brand_id = Column(Integer, ForeignKey('brands.brand_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    type: ProductType = relationship("ProductType", back_populates="products")
    brand: Brand = relationship('Brand', back_populates='products')
    product_detail: ProductDetail = relationship('ProductDetail', uselist=False, back_populates='product')
    more_image: List[Image] = relationship('Image', back_populates='product')
    orders: List[Order] = relationship('Order', secondary='order_product', back_populates='products')
    user: User = relationship('User', back_populates='products')