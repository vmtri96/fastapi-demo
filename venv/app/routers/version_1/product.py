from fastapi import APIRouter, Depends
import sqlalchemy as db
import sqlalchemy.orm
import app.my_session as my_session
from pydantic import parse_obj_as
from typing import List

from app.dto.product_dto import ProductDtoIn, ProductDtoOut
from app.repo.product_repo import ProductRepo
from app.model.product import Product
import app.dependencies.token_dependencies as token_dependencies

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel, Field

router = APIRouter()


async def get_product_repo(session: db.orm.Session = Depends(my_session.get_db)):
    return ProductRepo(session)


@router.post("/product")
async def create_product(product_dto: ProductDtoIn, product_repo: ProductRepo = Depends(get_product_repo)):
    product: Product = product_repo.save(product_dto)
    return ProductDtoOut.from_orm(product)


@router.get("/product/")
async def get_product_by_name(name: str = None, product_repo: ProductRepo = Depends(get_product_repo)):
    products: List[Product] = product_repo.get_product_by_name(name)
    products_out: List[ProductDtoOut] = parse_obj_as(List[ProductDtoOut], products)
    return products_out


class BasicQuery(BaseModel):
    price_lte: float = Field(..., example=5.2, alias="price[lte]")
    price_gte: float = Field(..., alias="price[gte]")


@router.get("/test")
def test(request: Request):
    query_params = request.query_params

    print(query_params)
    basic_query = BasicQuery(**query_params)
    print(basic_query)
    return {"virtual_host": request.headers, "params": basic_query}