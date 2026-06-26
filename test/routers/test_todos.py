from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.extensions import Base, get_db
from app.utils.auth_utils import get_current_user
from main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.models import Todos
import os

engine = create_engine(
    os.getenv("TEST_DATABASE_URL"),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "drewhundtest", "id": 1, "role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

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