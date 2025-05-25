from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import schema
from app.main import app
from jose import jwt
from dotenv import load_dotenv
import pytest

load_dotenv()
token_secret_key = os.getenv('SECRET_KEY_TOKEN')
algorithm = os.getenv('ALGORITHM')



    
def test_create_user(client):
    res = client.post("/users/", json={"email": "piratecaribiang@gmail.com", "password":"password9999"})
    new_user_test = schema.UserMsg(**res.json())
    
    assert new_user_test.email == "piratecaribiang@gmail.com"
    assert res.status_code == 201
    
def test_user_login(client,test_user):
    res = client.post("/login", data={"username": test_user["email"], "password":test_user["password"]})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,token_secret_key, algorithms=[algorithm])
    id = payload.get("user_id")
    
    assert id == test_user["id"]
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ('brendonstarkis@gmail.com', 'password123', 403),
    ('sonichedgehog@gmail.com', 'wrongpassword133131', 403),
    ('wrongemaigmai@gmail.com', 'wrongpassword', 403),
    (None, 'password9999', 403),
    ('sonichedgehog@gmail.com', None, 403)
])    
def test_incorent_login(client,test_user, email, password,status_code):
    res = client.post("/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
    
    