from datetime import timedelta, datetime, timezone
from typing import Annotated
from starlette import status
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from jose import jwt, JWTError
import os

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def authenticate_user(username: str, password: str, db, context):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not context.verify(password, user.hashed_password):
        return False

    return user

def create_access_token(
        username: str,
        user_id: int,
        role: str,
        expires_delta: timedelta
):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role
    }

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, os.getenv("APP_SECRET_KEY"), algorithm="HS256")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, os.getenv("APP_SECRET_KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")