from __future__ import annotations
import sqlalchemy as db
import sqlalchemy.orm

from app.model.product_type import ProductType
from app.dto.product_type_dto import ProductTypeDtoIn


class ProductTypeRepo(object):
    def __init__(self, session: db.orm.Session):
        self.sess: db.orm.Session = session


    def save(self, product_type: ProductTypeDtoIn):
        product_type_db = ProductType(name=product_type.name)
        self.sess.add(product_type_db)
        self.sess.commit()
        return product_type_db.type_id


    def get_all_product_type(self):
        return self.sess.query(ProductType).all()


    def delete_product_type(self, id: int):
        product_type: ProductType = self.sess.query(ProductType).filter(ProductType.type_id == id).first()
        self.sess.delete(product_type)
        self.sess.commit()
        return {"message": "delete successful product type id = " + str(id)}


