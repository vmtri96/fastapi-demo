from fastapi import APIRouter, Depends
import sqlalchemy as db
import sqlalchemy.orm
from pydantic import parse_obj_as
from typing import List

from app.repo.user_repo import UserRepo
from app.dto.user_dto import UserDtoOut, UserDtoIn, UserIdDelete, UserDtoUpdate
from app.model.user import User

import app.my_session as my_session
from app.dependencies.verify_user import is_admin, get_current_user_from_token, get_current_user_from_token_with_timeout


router = APIRouter()


async def get_user_repo(session: db.orm.Session = Depends(my_session.get_db)):
    return UserRepo(session)


@router.post("/users")
async def create_user(user_dto: UserDtoIn,
                      user_repo: UserRepo = Depends(get_user_repo)):
    user = user_repo.save(user_dto)
    jwt = token_dependencies.get_token(user)
    return {"access_token": jwt, "token_type": "bearer"}


@router.get("/users", dependencies=[Depends(is_admin)])
async def get_all_user(user_repo: UserRepo = Depends(get_user_repo)):
    all_users: List[User] = user_repo.get_all_user()
    users_out: List[UserDtoOut] = parse_obj_as(List[UserDtoOut], all_users)
    return users_out


@router.get("/users/{user_id}", dependencies=[Depends(get_current_user_from_token_with_timeout)])
async def get_user_by_id(user_id: int,
                         user_repo: UserRepo = Depends(get_user_repo)):
    user = user_repo.get_user_by_id(user_id)
    user_dto_out: UserDtoOut = parse_obj_as(UserDtoOut, user)
    return user_dto_out


# @router.delete("/users", dependencies=[Depends(is_admin)])
# async def delete_user(user_repo: UserRepo = Depends(get_user_repo)):
#     return user_repo.delete_user(user_id)
#
#
# @router.put("/users/{user_id}", dependencies=[Depends(get_current_user_from_token_with_timeout)])
# async def update_user(user_id: int, user_dto: UserDtoUpdate,
#                       user_repo: UserRepo = Depends(get_user_repo)):
#     return user_repo.update_user(user_id, user_dto)