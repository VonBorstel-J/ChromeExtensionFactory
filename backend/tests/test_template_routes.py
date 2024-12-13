# /backend/tests/test_templates_routes.py
import pytest
from app import app
from db import db
from models import User
from werkzeug.security import generate_password_hash
import jwt

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(email="temp@example.com", hashed_password=generate_password_hash("pass"))
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({"user_id": user.id}, app.config['JWT_SECRET'], algorithm="HS256")
    testing_client = app.test_client()
    return testing_client, token

def test_list_templates(client):
    c, token = client
    response = c.get('/templates/', headers={"Authorization": token})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
