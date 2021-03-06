from __future__ import annotations
from fastapi import HTTPException
import sqlalchemy.orm
import sqlalchemy as db

from app.dto.status_dto import StatusDtoIn, StatusDtoOut
from app.model.status import Status


class StatusRepo(object):
    def __init__(self, session: db.orm.Session):
        self.session = session


    def save(self, status_dto: StatusDtoIn):
        if not status_dto:
            raise HTTPException(status_code=400, detail="No input")

        status_in_db = self.get_status_by_name(status_dto.name)

        if status_in_db:
            raise HTTPException(status_code=400, detail="Status already exists")

        status: Status = Status(name=status_dto.name)
        self.session.add(status)
        self.session.commit()
        return status


    def get_status_by_name(self, name: str):
        return self.session.query(Status).filter(Status.name == name).first()
