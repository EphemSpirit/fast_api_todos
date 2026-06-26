from sqlalchemy import text
from fastapi import status
import pytest
from app.models import Todos
from test.test_database import client, TestingSessionLocal, engine

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Study every day",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

def test_read_all_authenticated(test_todo: Todos):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": "Learn to code", "description": "Study every day",
                                "priority": 5, "complete": False, "id": 1, "owner_id": 1}]


def test_read_one_authenticated(test_todo: Todos):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"title": "Learn to code", "description": "Study every day",
                                "priority": 5, "complete": False, "id": 1, "owner_id": 1}


def test_read_one_authenticated_not_found():
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo: Todos):
    request_data={
        "title": "New Todo",
        "description": "New todo description",
        "priority": 3,
        "complete": False,
    }
    response = client.post("/todos", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")
