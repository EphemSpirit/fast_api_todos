from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status
from app.extensions import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/")
async def get_user():
    return {"user": "authenticated"}