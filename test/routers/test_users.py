from test.utils import *
from app.extensions import get_db
from app.utils.auth_utils import get_current_user
from test.fixtures.users import test_user
from fastapi import status
from app.models import User

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user: User):
    res = client.get("/users")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["username"] == "test1234"
    assert res.json()["first_name"] == "Test"
    assert res.json()["last_name"] == "User"
    assert res.json()["email"] == "testemail@website.com"
    assert res.json()["phone_number"] == "123456789"
    assert res.json()["role"] == "admin"


def test_create_user(test_user: User):
    request_data = {
        "first_name": "Bojack",
        "last_name": "Horseman",
        "username": "horsinaround",
        "email": "horse@website.com",
        "password": "supersecret",
        "phone_number": "111-111-1111",
        "role": ""
    }

    res = client.post("users/", json=request_data)
    assert res.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()

    model = db.query(User).filter(User.id == 2).first()

    assert model.first_name == request_data.get("first_name")
    assert model.last_name == request_data.get("last_name")
    assert model.username == request_data.get("username")
    assert model.email == request_data.get("email")
    assert model.phone_number == request_data.get("phone_number")


def test_change_password_success(test_user: User):
    res = client.put("/users/reset_password", json={"password": "testpassword",
                                                    "new_password": "newpassword"})

    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    res = client.put("/users/reset_password", json={"password": "wrong",
                                                    "new_password": "newpassword"})

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    assert res.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    res = client.put("users/update_phone_number/2222222222")
    assert res.status_code == status.HTTP_204_NO_CONTENT