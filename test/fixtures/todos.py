import pytest
from app.models import Todos
from test.utils import TestingSessionLocal, engine
from sqlalchemy import text

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