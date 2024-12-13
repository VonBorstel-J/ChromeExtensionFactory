# /backend/tests/test_analytics.py
import pytest
from app import app
from db import db
from models import User, TemplateRating

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(email="analytics@test.com", hashed_password="hashed_pass")
        db.session.add(user)
        db.session.commit()
        ratings = [
            TemplateRating(user_id=user.id, template_name="web_scraper", rating=5),
            TemplateRating(user_id=user.id, template_name="web_scraper", rating=4),
            TemplateRating(user_id=user.id, template_name="tab_manager", rating=3),
        ]
        db.session.bulk_save_objects(ratings)
        db.session.commit()
    testing_client = app.test_client()
    return testing_client

def test_popular_templates(client):
    response = client.get('/analytics/popular-templates')
    assert response.status_code == 200
    data = response.get_json()
    assert {"template":"web_scraper","count":2} in data
    assert {"template":"tab_manager","count":1} in data
