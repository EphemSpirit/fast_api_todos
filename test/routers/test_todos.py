from fastapi import status

from app.extensions import get_db
from app.utils.auth_utils import get_current_user
from test.fixtures.todos import test_todo
from app.models import Todos
from test.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



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
    request_data = {
        "title": "New Todo",
        "description": "New todo description",
        "priority": 3,
        "complete": False,
    }
    response = client.post("/todos", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo: Todos):
    request_data = {
        "title": "Changed title",
        "description": "Study every day",
        "priority": 5,
        "complete": False
    }
    response = client.put("/todos/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Changed title"


def test_update_todo_not_found():
    request_data = {
        "title": "Changed title",
        "description": "Study every day",
        "priority": 5,
        "complete": False
    }
    response = client.put("/todos/100", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo: Todos):
    response = client.delete("/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todos/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
