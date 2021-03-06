from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy as db
import sqlalchemy.orm

import app.my_session as my_session
import app.dependencies.token_dependencies as token_dependencies
from app.repo.user_repo import UserRepo
from app.dto.user_dto import UserDtoOut


router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
                , session: db.orm.Session = Depends(my_session.get_db)):
    username = form_data.username
    user: UserDtoOut = token_dependencies.get_user(session, username)

    user_repo = UserRepo(session)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hash_password = user_repo.hash_password(form_data.password)

    if not hash_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt = token_dependencies.get_token(user)
    return {"access_token": jwt, "token_type": "bearer"}