from pydantic import BaseModel


class ProductTypeDtoIn(BaseModel):
    name: str


class ProductTypeDtoOut(BaseModel):
    type_id: int
    name: str

    class Config:
        orm_mode = True

