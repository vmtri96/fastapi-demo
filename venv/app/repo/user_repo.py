from __future__ import annotations
from fastapi import HTTPException
import sqlalchemy as db
import sqlalchemy.orm
from typing import Optional, List
import hashlib

from app.dto.user_dto import UserDtoIn, UserDtoUpdate, UserIdDelete
from app.model.user import User
from app.model.status import Status
from app.model.order import Order
from app.model.product import Product
from app.model.coupon import Coupon
from app.model.order_product import OrderProduct
from app.model.product_type import ProductType
from app.model.brand import Brand
from app.model.product_detail import ProductDetail
from app.model.image import Image


class UserRepo(object):
    def __init__(self, session: db.orm.Session):
        self.sess: db.orm.Session = session


    def save(self, user: UserDtoIn):
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user input")

        user_in_db = self.get_user_by_username(user.username)

        if user_in_db:
            raise HTTPException(status_code=400, detail="User already exists")
        user_db = User(username=user.username,
                       password=self.hash_password(user.password),
                       name=user.name,
                       phone=user.phone,
                       email=user.email,
                       role_id=user.role_id,
                       status_id=user.status_id)
        self.sess.add(user_db)
        self.sess.commit()
        return user_db


    def hash_password(self, password: str):
        hash_password: str = hashlib.sha256(password.encode()).hexdigest()
        return hash_password


    def get_all_user(self) -> List[User]:
        all_user: List[User] = self.sess.query(User).all()
        return all_user


    def get_user_by_id(self, id: int):
        return self.sess.query(User).filter(User.user_id == id).first()


    def get_user_by_username(self, username: str):
        return self.sess.query(User).filter(User.username == username).first()


    def delete_user(self, ids: UserIdDelete):
        for id in ids.user_id:
            user: User = self.sess.query(User).filter(User.user_id == id).first()
            self.sess.delete(user)
            self.sess.commit()
        return {"message": "Delete successful"}


    def update_user(self, id: int, user_dto: UserDtoUpdate):
        user: User = self.sess.query(User).filter(User.user_id == id).first()

        if user_dto.password is not None:
            user.password = user_dto.password
        if user_dto.name is not None:
            user.name = user_dto.name
        if user_dto.phone is not None:
            user.phone = user_dto.phone
        if user_dto.email is not None:
            user.email = user_dto.email
        self.sess.commit()
        return {"message": "Update successful"}
