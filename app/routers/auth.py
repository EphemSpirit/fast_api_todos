from fastapi import Depends, APIRouter
from app.extensions import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_utils import *

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post("/token")
async def get_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
        context=bcrypt_context
    )

    if not user:
        return 'Failed Authentication'

    return 'Successful authentication'


