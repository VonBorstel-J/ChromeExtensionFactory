# /backend/tests/test_auth.py
import pytest
from app import app
from db import db
from models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
    testing_client = app.test_client()
    yield testing_client

def test_signup(client):
    response = client.post('/auth/signup', json={"email":"newuser@test.com","password":"newpass"})
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data

def test_login_success(client):
    with app.app_context():
        user = User(email="login@test.com", hashed_password=generate_password_hash("loginpass"))
        db.session.add(user)
        db.session.commit()
    response = client.post('/auth/login', json={"email":"login@test.com","password":"loginpass"})
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data

def test_login_failure(client):
    response = client.post('/auth/login', json={"email":"nonexistent@test.com","password":"nopass"})
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid credentials"
