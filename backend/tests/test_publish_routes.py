# /backend/tests/test_publish_routes.py
import pytest
from app import app
from db import db
from models import User, Project
from werkzeug.security import generate_password_hash
import jwt
from config import Config
from unittest.mock import patch
import os

@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(email="publish@test.com", hashed_password=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({"user_id": user.id}, Config.JWT_SECRET, algorithm="HS256")
    testing_client = app.test_client()
    return testing_client, token, user.id

@patch('publish_routes.combine_templates')
@patch('publish_routes.boto3.client')
def test_publish_extension_success(mock_s3_client, mock_combine_templates, client):
    c, token, user_id = client
    project = Project(user_id=user_id, name="Publish Project", data={"templates": ["web_scraper"]})
    db.session.add(project)
    db.session.commit()
    
    mock_combine_templates.return_value = "/tmp/combined_templates"
    mock_s3_client.return_value.upload_file.return_value = True
    
    response = c.post(f'/publish/publish/{project.id}', headers={"Authorization": token})
    assert response.status_code == 200
    data = response.get_json()
    assert "download_url" in data

@patch('publish_routes.combine_templates')
@patch('publish_routes.boto3.client')
def test_publish_extension_project_not_found(mock_s3_client, mock_combine_templates, client):
    c, token, user_id = client
    response = c.post('/publish/publish/999', headers={"Authorization": token})
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Project not found"

@patch('publish_routes.combine_templates')
@patch('publish_routes.boto3.client')
def test_publish_extension_s3_failure(mock_s3_client, mock_combine_templates, client):
    c, token, user_id = client
    project = Project(user_id=user_id, name="Publish Project", data={"templates": ["web_scraper"]})
    db.session.add(project)
    db.session.commit()
    
    mock_combine_templates.return_value = "/tmp/combined_templates"
    mock_s3_client.return_value.upload_file.side_effect = Exception("S3 Upload Failed")
    
    response = c.post(f'/publish/publish/{project.id}', headers={"Authorization": token})
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Failed to upload extension"
