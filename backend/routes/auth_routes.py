from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User
from auth import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    user = User(email=email, hashed_password=password)
    db.session.add(user)
    db.session.commit()
    token = generate_token(user.id)
    return jsonify({"token": token})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.hashed_password, password):
        token = generate_token(user.id)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401
