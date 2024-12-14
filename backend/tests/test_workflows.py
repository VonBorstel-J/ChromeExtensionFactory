# /backend/tests/test_workflows.py
import pytest
from app import app
from db import db
from models import User, Project
from werkzeug.security import generate_password_hash
import jwt
from config import Config

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(email="workflow@test.com", hashed_password=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({"user_id": user.id}, Config.JWT_SECRET, algorithm="HS256")
    testing_client = app.test_client()
    return testing_client, token

def test_full_workflow(client):
    c, token = client

    # Create Project
    project_data = {
        "name": "Test Project",
        "data": {"templates": ["web_scraper", "tab_manager"]}
    }
    response = c.post('/projects/', json=project_data, headers={"Authorization": token})
    assert response.status_code == 201
    project = response.get_json()
    project_id = project["id"]

    # Publish Extension
    response = c.post(f'/publish/publish/{project_id}', headers={"Authorization": token})
    assert response.status_code == 200
    publish_data = response.get_json()
    assert "download_url" in publish_data

    # Download Extension
    response = c.get(f'/publish/download/{project_id}', headers={"Authorization": token})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/zip'

