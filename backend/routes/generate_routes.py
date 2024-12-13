# /backend/routes/generate_routes.py
from flask import Blueprint, request, jsonify
from tasks.celery_worker import async_generate_code
from auth import token_required
from schemas import CodeGenerationSchema

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/generate', methods=['POST'])
@token_required
def generate_code(current_user):
    data = request.get_json()
    validated_data = CodeGenerationSchema(**data)
    task = async_generate_code.delay(
        user_idea=validated_data.user_idea,
        template_type=validated_data.template_type,
        provider=validated_data.provider
    )
    return jsonify({"task_id": task.id}), 202
