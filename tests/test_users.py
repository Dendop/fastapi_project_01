from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import schema
from app.main import app
from .conftest import test_app, client
from jose import jwt
from dotenv import load_dotenv
import pytest

load_dotenv()
token_secret_key = os.getenv('SECRET_KEY_TOKEN')
algorithm = os.getenv('ALGORITHM')

@pytest.fixture
def test_user(client):
    user_data = {"email":"sonichedgehog@gmail.com", "password": "password9999"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    print(new_user)
    return new_user

    
def test_create_user(client):
    res = client.post("/users/", json={"email": "piratecaribiang@gmail.com", "password":"password9999"})
    new_user_test = schema.UserMsg(**res.json())
    
    assert new_user_test.email == "piratecaribiang@gmail.com"
    assert res.status_code == 201
    
def test_user_login(client,test_user):
    res = client.post("/login", data={"username": test_user["email"], "password":test_user["password"]})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,token_secret_key, algorithms=[algorithm])
    id: str = payload.get("user_id")
    
    assert res.status_code == 200
    