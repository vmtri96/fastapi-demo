from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import sqlalchemy as db
import sqlalchemy.orm
import jwt
import datetime

from app.dto.user_dto import UserDtoOut
import app.my_session as my_session
from app.dependencies.token_dependencies import decode_token, get_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ADMIN_ROLE_ID = 1
STORE_ROLE_ID = 3


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


def is_admin(user: UserDtoOut = Depends(get_current_user_from_token_with_timeout)):
    if user.role.role_id == ADMIN_ROLE_ID:
        return user
    raise HTTPException(status_code=400, detail="Not an expected user")


def is_store(user: UserDtoOut = Depends(get_current_user_from_token_with_timeout)):
    if user.role.role_id == STORE_ROLE_ID:
        return user
    raise HTTPException(status_code=400, detail="Not an expected user")