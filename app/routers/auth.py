from fastapi import APIRouter
from pydantic import BaseModel
from app.extensions import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_utils import *
from datetime import timedelta
from starlette import status

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token)
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    token = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=20))

    return {"access_token": token, "token_type": "Bearer"}


