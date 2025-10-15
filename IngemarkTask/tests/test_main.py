from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_message():
    response = client.post(
        "/messages/",
        headers={"X-API-Key": "secret-key"},
        json={
            "chat_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "content": "Hello, test!",
            "sent_at": "2025-10-09T10:00:00Z",
            "role": "user",
            "rating": False
        }
    )
    if response.status_code != 200:
        print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, test!"
    assert "message_id" in data

def test_read_messages():
    client.post(
        "/messages/",
        headers={"X-API-Key": "secret-key"},
        json={
            "chat_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "content": "Test message",
            "sent_at": "2025-10-09T10:00:00Z",
            "role": "user",
            "rating": False
        }
    )
    
    response = client.get("/messages/", headers={"X-API-Key": "secret-key"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["content"] == "Test message"

def test_update_message():
    post_response = client.post(
        "/messages/",
        headers={"X-API-Key": "secret-key"},
        json={
            "chat_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "content": "Original message",
            "sent_at": "2025-10-09T10:00:00Z",
            "role": "ai",
            "rating": False
        }
    )
    message_id = post_response.json()["message_id"]

    update_response = client.put(
        f"/messages/{message_id}",
        headers={"X-API-Key": "secret-key"},
        json={
            "chat_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "content": "Update test!",
            "sent_at": "2025-10-09T10:00:00Z",
            "role": "ai",
            "rating": True
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["content"] == "Update test!"
    assert data["rating"] == True
