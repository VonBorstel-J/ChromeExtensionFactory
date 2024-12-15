# /backend/tests/test_payments.py
import pytest
from app import app
from db import db
from models import User
from werkzeug.security import generate_password_hash
import jwt
from config import Config

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(email="paytest@example.com", hashed_password=generate_password_hash("pass"), subscription_tier="free")
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({"user_id": user.id}, Config.JWT_SECRET, algorithm="HS256")
    testing_client = app.test_client()
    yield testing_client, token, user.id

def test_subscribe_invalid_tier(client):
    c, token, user_id = client
    response = c.post('/payments/subscribe', json={"tier": "gold", "payment_confirmation": "abc"}, headers={"Authorization": token})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid tier selected"

def test_subscribe_missing_payment_confirmation(client):
    c, token, user_id = client
    response = c.post('/payments/subscribe', json={"tier": "pro"}, headers={"Authorization": token})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Payment confirmation is required"

def test_subscribe_success(client):
    c, token, user_id = client
    response = c.post('/payments/subscribe', json={"tier": "pro", "payment_confirmation": "valid_payment"}, headers={"Authorization": token})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Subscription updated successfully"
    assert data["tier"] == "pro"
