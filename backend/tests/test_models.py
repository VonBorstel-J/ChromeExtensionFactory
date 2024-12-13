# /backend/tests/test_models.py
import pytest
from db import db
from models import User, Project, TemplateRating

def test_user_model():
    user = User(email="user@test.com", hashed_password="hashed_pass")
    db.session.add(user)
    db.session.commit()
    retrieved_user = User.query.filter_by(email="user@test.com").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "user@test.com"

def test_project_model():
    user = User(email="project@test.com", hashed_password="hashed_pass")
    db.session.add(user)
    db.session.commit()
    project = Project(user_id=user.id, name="Test Project", data={"key": "value"})
    db.session.add(project)
    db.session.commit()
    retrieved_project = Project.query.filter_by(name="Test Project").first()
    assert retrieved_project is not None
    assert retrieved_project.data["key"] == "value"

def test_template_rating_model():
    user = User(email="rating@test.com", hashed_password="hashed_pass")
    db.session.add(user)
    db.session.commit()
    rating = TemplateRating(user_id=user.id, template_name="web_scraper", rating=5)
    db.session.add(rating)
    db.session.commit()
    retrieved_rating = TemplateRating.query.filter_by(template_name="web_scraper").first()
    assert retrieved_rating is not None
    assert retrieved_rating.rating == 5
