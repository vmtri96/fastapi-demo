from fastapi import APIRouter, Depends
import sqlalchemy as db
import sqlalchemy.orm
from pydantic import parse_obj_as
from typing import List

from app.dto.status_dto import StatusDtoIn, StatusDtoOut
from app.model.status import Status
from app.repo.status_repo import StatusRepo

import app.my_session as my_session
from app.dependencies.verify_user import is_admin, get_current_user_from_token_with_timeout, get_current_user_from_token


router = APIRouter()


async def get_status_repo(session: db.orm.Session = Depends(my_session.get_db)):
    return StatusRepo(session)


@router.post("/status", dependencies=[Depends(is_admin)])
async def create_status(status_dto: StatusDtoIn,
                        status_repo: StatusRepo = Depends(get_status_repo)):
    status: Status = status_repo.save(status_dto)
    return StatusDtoOut.from_orm(status)