from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import schema
from app.main import app
from .conftest import test_app, client




def test_root(client):
    res = client.get("/")
    print(res.json())
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "sonichedgehog@gmail.com", "password":"password9999"})
    new_user_test = schema.UserMsg(**res.json())
    
    assert new_user_test.email == "sonichedgehog@gmail.com"
    assert res.status_code == 201