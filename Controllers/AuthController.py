from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from pydantic import ValidationError
from functools import wraps
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt

from Utils.schemas import TokenPayload

controllerName = "auth"
authController = APIRouter()

class User:
    def __init__(self, name, age):
        self.login = name
        self.password = age

users = []
users.append(User('user', 'password'))
users.append(User('user12', 'test'))
users.append(User('users', 'pass'))

key = '1EU1jBxj8nKfvCaAzdeq1yafPEGrimcg8k'

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> str:
    try:
        payload = jwt.decode(
            token, key, algorithms=['HS256']
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = next(
        (obj for obj in users if obj.login == token_data.sub),
        None
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return result.login


class RequestLogin(BaseModel):
    login: str
    password: str


def create_access_token(subject: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=120)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key, 'HS256')
    return encoded_jwt

@authController.post(f'/{controllerName}/login/')
def login(login: str = Form(), password: str = Form()):
    if not login or not password:
        return 'Bad credentials', 401

    result = next(
        (obj for obj in users if obj.login == login and obj.password == password),
        None
    )
    if result is None:
        return 'Bad credentials', 401

    return {"access_token": create_access_token(login)}
