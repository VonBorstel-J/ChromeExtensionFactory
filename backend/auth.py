# /backend/auth.py
import jwt
from flask import request, jsonify, current_app
from functools import wraps
from models import User
from db import db

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return jsonify({"error": "Token missing"}), 401
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=["HS256"])
            user_id = data['user_id']
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 401
            return f(user, *args, **kwargs)
        except Exception:
            return jsonify({"error": "Invalid Token"}), 401
    return decorator

def generate_token(user_id):
    import datetime
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm="HS256")
