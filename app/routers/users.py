from fastapi import Depends, APIRouter
from starlette import status
from app.extensions import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import CreateUserRequest
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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