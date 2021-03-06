from pydantic import BaseModel
from datetime import datetime

from app.dto.user_dto import UserDtoOut
from app.dto.product_type_dto import ProductTypeDtoOut
from app.dto.brand_dto import BrandDtoOut


class ProductDtoIn(BaseModel):
    name: str
    description: str
    price: int
    image: str
    quantity: int
    import_date: datetime
    import_price: int
    type_id: int
    brand_id: int
    user_id: int


class ProductDtoOut(BaseModel):
    product_id: int
    name: str
    description: str
    price: int
    image: str
    quantity: int
    import_date: datetime
    import_price: int
    type: ProductTypeDtoOut
    brand: BrandDtoOut
    user: UserDtoOut

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True