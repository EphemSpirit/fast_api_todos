from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status
from app.extensions import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import Todos
from app.schemas import TodoRequest
from app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_id: int = Path(gt=0)
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.delete(todo)
    db.commit()