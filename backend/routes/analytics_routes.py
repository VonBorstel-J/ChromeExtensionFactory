# /backend/routes/analytics_routes.py
from flask import Blueprint, jsonify
from auth import token_required
from analytics import get_popular_templates

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/popular-templates', methods=['GET'])
@token_required
def popular_templates(current_user):
    data = get_popular_templates(db)
    return jsonify(data)
