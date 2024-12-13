# /backend/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get("JWT_SECRET", "changeme")
    API_KEY = os.environ.get("API_KEY", "changeme")

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    S3_REGION = os.environ.get("S3_REGION")

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

    STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

    CHROME_WEBSTORE_CLIENT_ID = os.environ.get("CHROME_WEBSTORE_CLIENT_ID")
    CHROME_WEBSTORE_CLIENT_SECRET = os.environ.get("CHROME_WEBSTORE_CLIENT_SECRET")
    CHROME_WEBSTORE_REFRESH_TOKEN = os.environ.get("CHROME_WEBSTORE_REFRESH_TOKEN")

