from __future__ import annotations
import sqlalchemy as db
import sqlalchemy.orm

from app.dto.role_dto import RoleDtoIn
from app.model.role import Role


class RoleRepo(object):
    def __init__(self, session: db.orm.Session):
        self.sess: db.orm.Session = session


    def save(self, role_dto: RoleDtoIn):
        role: Role = Role(name=role_dto.name)
        self.sess.add(role)
        self.sess.commit()
        return role.role_id


    def get_all_role(self):
        return self.sess.query(Role).all()


    def delete_role(self, id: int):
        role = self.sess.query(Role).filter(Role.role_id == id).first()
        self.sess.delete(role)
        self.sess.commit()
        return {"message": "delete successful role id = " + str(id)}


    def update_role(self, id: int, role_dto: RoleDtoIn):
        role: Role = self.sess.query(Role).filter(Role.role_id == id).first()
        role.name = role_dto.name
        self.sess.commit()
        return {"message": "update successful role id = " + str(id)}