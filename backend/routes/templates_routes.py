# /backend/routes/templates_routes.py
from flask import Blueprint, jsonify, request
from auth import token_required
import os
from werkzeug.utils import secure_filename

templates_bp = Blueprint('templates', __name__)

ALLOWED_EXTENSIONS = {'json', 'js'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@templates_bp.route('/', methods=['GET'])
@token_required
def list_templates(current_user):
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    available = [d for d in os.listdir(template_path) if os.path.isdir(os.path.join(template_path, d))]
    return jsonify(available)

@templates_bp.route('/upload', methods=['POST'])
@token_required
def upload_template(current_user):
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .json or .js allowed."}), 400

    filename = secure_filename(file.filename)
    user_upload_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'user_uploads', str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)
    file.save(os.path.join(user_upload_dir, filename))

    return jsonify({"message": "File uploaded successfully"}), 200
