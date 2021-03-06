from __future__ import annotations
import sqlalchemy.orm
import sqlalchemy as db
from fastapi import HTTPException
from typing import List

from app.dto.brand_dto import BrandDtoIn, BrandDtoOut, BrandDtoUpdate
from app.model.brand import Brand


class BrandRepo(object):
    def __init__(self, session: db.orm.Session):
        self.session: db.orm.Session = session


    def save(self, brand_dto: BrandDtoIn):
        if not brand_dto:
            raise HTTPException(status_code=400, detail="No input")

        brand_in_db = self.get_brand_by_name(brand_dto.name)

        if brand_in_db:
            raise HTTPException(status_code=400, detail="Brand already exists")

        brand: Brand = Brand(name=brand_dto.name, country=brand_dto.country)
        self.session.add(brand)
        self.session.commit()
        return brand


    def get_all_brand(self):
        all_brand: List[Brand] = self.session.query(Brand).all()
        return all_brand


    def get_brand_by_name(self, name: str):
        brand: Brand = self.session.query(Brand).filter(Brand.name == name).first()
        return brand


    def update_brand(self, id: int, brand_dto: BrandDtoUpdate):
        brand: Brand = self.session.query(Brand).filter(Brand.brand_id == id).first()

        if brand_dto.name is not None:
            brand.name = brand_dto.name
        if brand_dto.country is not None:
            brand.country = brand_dto.country
        self.session.commit()
        return {"message": "Update successful"}


    def delete_brand(self, id: int):
        brand: Brand = self.session.query(Brand).filter(Brand.brand_id == id).first()

        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        self.session.delete(brand)
        self.session.commit()
        return {"message": "Delete successful"}
