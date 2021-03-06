from pydantic import BaseModel
from typing import Optional, List

from app.dto.status_dto import StatusDtoOut
from app.dto.role_dto import RoleDtoOut


class UserDtoIn(BaseModel):
    username: str
    password: str
    name: str
    phone: str
    email: str
    role_id: int
    status_id: int


class UserDtoUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    role_id: Optional[int]
    status_id: Optional[int]


class UserIdDelete(BaseModel):
    user_id: List[int]


class UserDtoOut(BaseModel):
    user_id: int
    name: str
    phone: str
    email: str
    role: RoleDtoOut
    status: StatusDtoOut

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

