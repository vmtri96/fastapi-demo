from pydantic import BaseModel
from typing import Optional


class BrandDtoIn(BaseModel):
    name: str
    country: str


class BrandDtoOut(BaseModel):
    brand_id: int
    name: str
    country: str

    class Config:
        orm_mode=True


class BrandDtoUpdate(BaseModel):
    name: Optional[str]
    country: Optional[str]