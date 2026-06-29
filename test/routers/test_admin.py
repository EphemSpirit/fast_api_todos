from test.utils import *
from app.extensions import get_db
from app.utils.auth_utils import get_current_user
from test.fixtures.todos import test_todo
from fastapi import status
from app.models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    res = client.get("/admin/todo")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [{"complete": False, "title": "Learn to code", "description": "Study every day", "id": 1, "priority": 5, "owner_id": 1}]


def test_admin_delete_todo_authenticated(test_todo):
    res = client.delete("admin/todo/1")
    assert res.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


def test_admin_delete_todo_not_found():
    res = client.delete("/admin/todo/10000")
    assert res.status_code == status.HTTP_404_NOT_FOUND

    assert res.json() == {"detail": "Todo not found."}