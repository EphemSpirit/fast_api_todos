import pytest
from app.models import User
from app.routers.users import bcrypt_context
from test.utils import TestingSessionLocal, engine
from sqlalchemy import text


@pytest.fixture
def test_user():
    user = User(
        first_name="Test",
        last_name="User",
        email="testemail.website.com",
        username="test1234",
        is_active=True,
        role="",
        phone_number="123456789",
        hashed_password=bcrypt_context.hash("testpassword")
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()