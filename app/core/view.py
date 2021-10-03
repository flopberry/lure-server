from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app import constants
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.HASH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    expire: int = payload.get("exp")
    if not expire or expire < datetime.utcnow().timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await User.filter(login=username).get_or_none()
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=int(constants.ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constants.SECRET_KEY, algorithm=constants.HASH_ALGORITHM)
    return encoded_jwt
