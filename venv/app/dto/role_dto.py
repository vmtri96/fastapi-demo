from pydantic import BaseModel


class RoleDtoIn(BaseModel):
    name: str


class RoleDtoOut(BaseModel):
    role_id: int
    name: str

    class Config:
        orm_mode = True

