from fastapi import Depends, APIRouter, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from app.extensions import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import CreateUserRequest
from passlib.context import CryptContext
from app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_request: CreateUserRequest):
    new_user = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(new_user)
    db.commit()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    user_model = db.query(User).filter(User.id == user.get("id")).first()

    return user_model

@router.put("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()
