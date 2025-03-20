# /backend/models.py
from db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    is_premium = db.Column(db.Boolean, default=False, index=True)
    # NEW FIELD: subscription_tier
    subscription_tier = db.Column(db.String(20), default="free", index=True)  # free, pro, enterprise

    projects = db.relationship('Project', backref='user', lazy=True)
    ratings = db.relationship('TemplateRating', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_premium": self.is_premium,
            "subscription_tier": self.subscription_tier
        }

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    name = db.Column(db.String(200), index=True)
    data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "data": self.data,
            "created_at": self.created_at.isoformat()
        }

class TemplateRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    template_name = db.Column(db.String(200), index=True)
    rating = db.Column(db.Integer, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "template_name": self.template_name,
            "rating": self.rating
        }
