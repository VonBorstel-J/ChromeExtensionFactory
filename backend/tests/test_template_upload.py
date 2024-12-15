# /backend/tests/test_template_upload.py
import pytest
from app import app
from db import db
from models import User
from werkzeug.security import generate_password_hash
import jwt
from config import Config
import io

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(email="uploadtest@example.com", hashed_password=generate_password_hash("pass"))
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({"user_id": user.id}, Config.JWT_SECRET, algorithm="HS256")
    testing_client = app.test_client()
    yield testing_client, token, user.id

def test_upload_no_file(client):
    c, token, user_id = client
    response = c.post('/templates/upload', headers={"Authorization": token})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No file provided"

def test_upload_invalid_file_type(client):
    c, token, user_id = client
    data = {
        'file': (io.BytesIO(b"dummy content"), 'test.txt')
    }
    response = c.post('/templates/upload', data=data, content_type='multipart/form-data', headers={"Authorization": token})
    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid file type" in data["error"]

def test_upload_success(client):
    c, token, user_id = client
    data = {
        'file': (io.BytesIO(b"{}"), 'config.json')
    }
    response = c.post('/templates/upload', data=data, content_type='multipart/form-data', headers={"Authorization": token})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "File uploaded successfully"
