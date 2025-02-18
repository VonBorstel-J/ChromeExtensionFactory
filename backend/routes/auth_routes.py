from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User
from auth import generate_token
from schemas import UserSignupSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        # Validate input using Pydantic schema
        validated_data = UserSignupSchema(**data)
    except Exception as e:
        # Return a clear error message if validation fails
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    email = validated_data.email
    password = generate_password_hash(validated_data.password)
    # Force subscription_tier to "free" on signup
    user = User(email=email, hashed_password=password, subscription_tier="free")
    db.session.add(user)
    db.session.commit()
    token = generate_token(user.id)
    return jsonify({"token": token}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        validated_data = UserLoginSchema(**data)
    except Exception as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    email = validated_data.email
    password = validated_data.password
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.hashed_password, password):
        token = generate_token(user.id)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
