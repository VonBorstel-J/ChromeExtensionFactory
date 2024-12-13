# /backend/routes/projects_routes.py
from flask import Blueprint, request, jsonify
from auth import token_required
from models import Project
from db import db
from schemas import ProjectSchema

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/', methods=['GET'])
@token_required
def get_projects(current_user):
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return jsonify([project.to_dict() for project in projects])

@projects_bp.route('/', methods=['POST'])
@token_required
def create_project(current_user):
    data = request.get_json()
    validated_data = ProjectSchema(**data)
    project = Project(
        user_id=current_user.id,
        name=validated_data.name,
        data=validated_data.data
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201
