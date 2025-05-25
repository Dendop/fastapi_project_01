import pytest
from .test_database import engine, TestingSessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import model

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
        
@pytest.fixture()
def test_user(client):
    user_data = {"email":"sonichedgehog@gmail.com", "password": "password9999"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    print(new_user)
    return new_user
     
@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})
    
@pytest.fixture()   
def authorized_client(client,token):
    client.headers = {**client.headers,"Authorization": f"Bearer {token}"}
    return client

@pytest.fixture()
def test_posts(test_user,session):
    post_data = [
        {
            "title":"my favourite chair",
            "content": "ofcourse it's and irone throne",
            "user_id": test_user["id"]
        },
        {
            "title": "unjustice",
            "content": "I was prosecuted by the kind in the king's landing",
            "user_id": test_user["id"]    
        },
        {
            "title": "I saw it",
            "content": "my father was executed in the king's landing",
            "user_id": test_user["id"]
        }
    ]
    def create_post_model(post): #function to convert dict into Post model
         return model.Post(**post)
     
    post_map = map(create_post_model, post_data) #apply Post model for each dict
    posts = list(post_map) #convert map object into list
    session.add_all(posts)
    session.commit()
    posts = session.query(model.Post).all()
    print(f"Posts in database {posts}")
    return posts