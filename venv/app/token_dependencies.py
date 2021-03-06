from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
import datetime

import sqlalchemy as db
import sqlalchemy.orm
import jwt

import app.my_session as my_session
from app.dto.user_dto import UserDtoIn, UserDtoOut
from app.model.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

ACCESS_TOKEN_EXPIRE_MINUTES = 60


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


def get_current_user_from_token(token: str = Depends(oauth2_scheme), session: db.orm.Session = Depends(my_session.get_db)):
    user: UserDtoOut = decode_token(session, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def get_current_user_from_token_with_timeout(token: str = Depends(oauth2_scheme), session: db.orm.Session = Depends(my_session.get_db)):
    try:
        decoded: dict = jwt.decode(token, "secret")
    except:
        raise HTTPException(status_code=400, detail="Invalid token")

    issue_date: str = decoded['issue_date']
    timestamp: datetime = datetime.datetime.strptime(issue_date, "%Y-%m-%dT%H:%M:%S.%f")

    if datetime.datetime.now() - timestamp >= datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
        raise HTTPException(status_code=400, detail="Token expired")
    username = decoded['user']

    user: UserDtoOut = get_user(session, username)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    return user


def verify_admin(user: UserDtoOut = Depends(get_current_user_from_token_with_timeout)):
    if user.role.name == "admin":
        return user
    raise HTTPException(status_code=400, detail="Not an expected user")