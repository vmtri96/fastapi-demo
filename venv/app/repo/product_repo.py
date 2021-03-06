from __future__ import annotations
from fastapi import HTTPException
import sqlalchemy as db
import sqlalchemy.orm
from typing import List

from app.dto.product_dto import ProductDtoIn, ProductDtoOut
from app.model.product import Product


class ProductRepo(object):
    def __init__(self, session: db.orm.Session):
        self.session = session

    def save(self, product_dto: ProductDtoIn):
        if not product_dto:
            raise HTTPException(status_code=400, detail="No input")

        product_existed = self.get_product_by_name_and_store(product_dto.name, product_dto.user_id)
        if product_existed:
            raise HTTPException(status_code=400, detail="Product already exists")

        product: Product = Product(name=product_dto.name,
                                   description=product_dto.description,
                                   price=product_dto.price,
                                   image=product_dto.image,
                                   quantity=product_dto.quantity,
                                   import_date=product_dto.import_date,
                                   import_price=product_dto.import_price,
                                   type_id=product_dto.type_id,
                                   brand_id=product_dto.brand_id,
                                   user_id=product_dto.user_id)
        self.session.add(product)
        self.session.commit()
        return product


    def get_product_by_id(self, id: int):
        return self.session.query(Product).filter(Product.id == id).first()


    def get_product_by_name_and_store(self, name: str, user_id: int):
        return self.session.query(Product).filter(Product.name.like(f'%{name}%')).all()


    def get_product_by_name(self, name: str):
        product: List[Product] = self.session.query(Product).filter(Product.name.like(f'%{name}%')).all()
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        return product