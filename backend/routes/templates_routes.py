# /backend/routes/templates_routes.py
from flask import Blueprint, jsonify
from auth import token_required
import os

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/', methods=['GET'])
@token_required
def list_templates(current_user):
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    available = [d for d in os.listdir(template_path) if os.path.isdir(os.path.join(template_path, d))]
    return jsonify(available)
