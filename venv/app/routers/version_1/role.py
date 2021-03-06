from fastapi import APIRouter, Depends
import sqlalchemy as db
import sqlalchemy.orm
from pydantic import parse_obj_as
from typing import List

from app.dto.role_dto import RoleDtoIn, RoleDtoOut
from app.repo.role_repo import RoleRepo

import app.my_session as my_session
from app.dependencies.verify_user import is_admin, get_current_user_from_token_with_timeout, get_current_user_from_token


router = APIRouter()


async def get_role_repo(session: db.orm.Session = Depends(my_session.get_db)):
    return RoleRepo(session)


@router.post("/roles")
async def create_role(role_dto: RoleDtoIn,
                      role_repo: RoleRepo = Depends(get_role_repo)):
    id = role_repo.save(role_dto)
    out_dict: dict = role_dto.dict()
    out_dict['role_id'] = id
    role_out = RoleDtoOut(**out_dict)
    return role_out


@router.get("/roles", dependencies=[Depends(is_admin)])
async def get_all_role(role_repo: RoleRepo = Depends(get_role_repo)):
    roles: List[Role] = role_repo.get_all_role()
    roles_out: List[RoleDtoOut] = parse_obj_as(List[RoleDtoOut], roles)
    return roles_out


@router.delete("/roles/{role_id}", dependencies=[Depends(is_admin)])
async def delete_role(role_id: int,
                      role_repo: RoleRepo = Depends(get_role_repo)):
    return role_repo.delete_role(role_id)


@router.put("/roles/{role_id}", dependencies=[Depends(is_admin)])
async def update_role(role_id: int, role_dto: RoleDtoIn,
                      role_repo: RoleRepo = Depends(get_role_repo)):
    return role_repo.update_role(role_id, role_dto)