from jose import jwt
from app.schemas import users as usersSchema 
from app.schemas import auth as authSchema
from app.config import settings
import pytest

def test_create_user(client):
    response = client.post("/users/", json={"email": "testuser@gmail.com", "password": "test123"})
    new_user = usersSchema.UserResponse(**response.json())
    assert response.status_code == 201

def test_login_usr(client,test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_response = authSchema.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('testuser@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('testuser@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code