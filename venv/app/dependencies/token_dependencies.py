from fastapi import Depends, HTTPException, status

from fastapi.encoders import jsonable_encoder
import datetime

import sqlalchemy as db
import sqlalchemy.orm
import jwt

import app.my_session as my_session
from app.dto.user_dto import UserDtoIn, UserDtoOut
from app.model.user import User





def get_user(session: db.orm.Session, username: str):
    user: User = session.query(User).filter(User.username == username).first()
    session.add(user)
    session.commit()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return UserDtoOut.from_orm(user)


def get_token(user: UserDtoIn):
    payload = {"user": user.username, "issue_date": datetime.datetime.now()}
    json_compatible = jsonable_encoder(payload)
    encoded_jwt = jwt.encode(json_compatible, 'secret', algorithm='HS256')
    return encoded_jwt


def decode_token(session: db.orm.Session, token: str):
    try:
        decoded: dict = jwt.decode(token, "secret")
    except:
        raise HTTPException(status_code=400, detail="Invalid token")

    username = decoded['user']
    user: UserDtoOut = get_user(session, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    return user




