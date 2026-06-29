from test.utils import *
from app.utils.auth_utils import authenticate_user, create_access_token, get_current_user
from app.extensions import get_db
from test.fixtures.users import test_user
from app.routers.users import bcrypt_context
from jose import jwt
from datetime import timedelta
import os
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "testpassword", db, bcrypt_context)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("wrong", "testpassword", db, bcrypt_context)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrong", db, bcrypt_context)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token,
                               os.getenv("APP_SECRET_KEY"),
                               algorithms=["HS256"], options={"verify_signature": False}
                               )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, os.getenv("APP_SECRET_KEY"), algorithm="HS256")
    user = await get_current_user(token=token)

    assert user == {"username": "testuser", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, os.getenv("APP_SECRET_KEY"), algorithm="HS256")
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"