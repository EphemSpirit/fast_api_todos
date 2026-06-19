from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status
from app.extensions import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import Todos
from app.schemas import TodoRequest
from app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)], todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo is not None:
        return todo

    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_body: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    new_todo = Todos(**todo_body.model_dump(), owner_id=user.get("id"))
    db.add(new_todo)
    db.commit()


@router.put("/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def update_todo(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_request: TodoRequest,
        todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()


@router.delete("/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(
        user: Annotated[dict, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
