from pydantic import BaseModel


class StatusDtoIn(BaseModel):
    name: str


class StatusDtoOut(BaseModel):
    status_id: int
    name: str

    class Config:
        orm_mode = True