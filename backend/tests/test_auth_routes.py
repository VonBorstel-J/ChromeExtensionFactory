# /backend/tests/test_auth_routes.py
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
    response = client.post('/auth/signup', json={"email":"test@example.com","password":"secret"})
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data

def test_login(client):
    with app.app_context():
        user = User(email="test2@example.com", hashed_password=generate_password_hash("pass"))
        db.session.add(user)
        db.session.commit()
    response = client.post('/auth/login', json={"email":"test2@example.com","password":"pass"})
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
