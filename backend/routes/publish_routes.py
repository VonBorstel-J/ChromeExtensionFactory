# /backend/routes/publish_routes.py
from flask import Blueprint, request, jsonify, send_file
from auth import token_required
from models import Project
from db import db
from templates_service import combine_templates
import os
import zipfile
import tempfile
import shutil
import boto3
from config import Config
import logging

publish_bp = Blueprint('publish', __name__)

@publish_bp.route('/publish/<int:project_id>', methods=['POST'])
@token_required
def publish_extension(current_user, project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        logging.warning(f"Publish failed: Project ID {project_id} not found for user ID {current_user.id}")
        return jsonify({"error": "Project not found"}), 404

    template_names = project.data.get("templates", [])
    base_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    combined_dir = combine_templates(template_names, base_path)

    # Zip the extension files
    zip_path = os.path.join(tempfile.gettempdir(), f"extension_{project_id}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(combined_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, combined_dir))

    # Upload to AWS S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.S3_REGION
    )
    s3_key = f"extensions/extension_{project_id}.zip"
    try:
        s3_client.upload_file(zip_path, Config.S3_BUCKET_NAME, s3_key, ExtraArgs={'ACL': 'public-read'})
    except Exception as e:
        logging.error(f"Failed to upload to S3: {str(e)}")
        return jsonify({"error": "Failed to upload extension"}), 500

    # Generate download URL
    download_url = f"https://{Config.S3_BUCKET_NAME}.s3.{Config.S3_REGION}.amazonaws.com/{s3_key}"

    # Cleanup
    os.remove(zip_path)
    shutil.rmtree(combined_dir)

    logging.info(f"Extension {project_id} published successfully by user {current_user.id}")
    return jsonify({"download_url": download_url}), 200

@publish_bp.route('/download/<int:project_id>', methods=['GET'])
@token_required
def download_extension(current_user, project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        logging.warning(f"Download failed: Project ID {project_id} not found for user ID {current_user.id}")
        return jsonify({"error": "Project not found"}), 404

    zip_path = os.path.join(tempfile.gettempdir(), f"extension_{project_id}.zip")

    # Check if zip exists
    if not os.path.exists(zip_path):
        logging.warning(f"Download failed: Extension ZIP for project ID {project_id} does not exist")
        return jsonify({"error": "Extension not published yet"}), 400

    logging.info(f"Extension {project_id} downloaded by user {current_user.id}")
    return send_file(zip_path, as_attachment=True, attachment_filename=f"extension_{project_id}.zip")
