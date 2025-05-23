import pytest
from .test_database import Base, engine
from app.main import app
from fastapi.testclient import TestClient



@pytest.fixture(scope="module")
def test_app():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture(scope="module")
def client(test_app):
    with TestClient(test_app) as client:
        yield client
    