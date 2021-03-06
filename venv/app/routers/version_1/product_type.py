from fastapi import APIRouter, Depends
import sqlalchemy as db
import sqlalchemy.orm
from pydantic import parse_obj_as
from typing import List

from app.dto.product_type_dto import ProductTypeDtoIn, ProductTypeDtoOut
from app.repo.product_type_repo import ProductTypeRepo
from app.model.product_type import ProductType

import app.my_session as my_session
from app.dependencies.verify_user import is_admin, get_current_user_from_token, get_current_user_from_token_with_timeout

router = APIRouter()


async def get_product_type_repo(session: db.orm.Session = Depends(my_session.get_db)):
    return ProductTypeRepo(session)


@router.post("/product-type", dependencies=[Depends(get_current_user_from_token_with_timeout)])
async def create_product_type(product_type_dto: ProductTypeDtoIn,
                              product_type_repo: ProductTypeRepo = Depends(get_product_type_repo)):
    id: int = product_type_repo.save(product_type_dto)
    out_dict: dict = product_type_dto.dict()
    out_dict['type_id'] = id
    product_type_out: ProductTypeDtoOut = parse_obj_as(ProductTypeDtoOut, out_dict)
    return product_type_out


@router.get("/product-type", dependencies=[Depends(get_current_user_from_token_with_timeout)])
async def get_all_product_type(product_type_repo: ProductTypeRepo = Depends(get_product_type_repo)):
    product_type: List[ProductType] = product_type_repo.get_all_product_type()
    product_type_out: List[ProductTypeDtoOut] = parse_obj_as(List[ProductTypeDtoOut], product_type)
    return product_type_out


@router.delete("/product-type/{type_id}", dependencies=[Depends(is_admin)])
async def delete_product_type(type_id: int, product_type_repo: ProductTypeRepo = Depends(get_product_type_repo)):
    return product_type_repo.delete_product_type(type_id)