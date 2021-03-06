from fastapi import APIRouter, Depends
import sqlalchemy as db
import sqlalchemy.orm
from pydantic import parse_obj_as
from typing import List

from app.dto.brand_dto import BrandDtoIn, BrandDtoOut
from app.model.brand import Brand
from app.repo.brand_repo import BrandRepo

import app.my_session as my_session
from app.dependencies.verify_user import is_admin, get_current_user_from_token_with_timeout


router = APIRouter()


async def get_brand_repo(session: db.orm.Session = Depends(my_session.get_db)):
    return BrandRepo(session)


@router.post("/brands", dependencies=[Depends(is_admin)])
async def create_brand(brand_dto: BrandDtoIn,
                       brand_repo: BrandRepo = Depends(get_brand_repo)):
    brand: Brand = brand_repo.save(brand_dto)
    return BrandDtoOut.from_orm(brand)


@router.get("/brands", dependencies=[Depends(get_current_user_from_token_with_timeout)])
async def get_all_brand(brand_repo: BrandRepo = Depends(get_brand_repo)):
    all_brand: List[Brand] = brand_repo.get_all_brand()
    brand_out: List[BrandDtoOut] = parse_obj_as(List[BrandDtoOut], all_brand)
    return brand_out