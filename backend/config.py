# /backend/config.py
import os
from google.cloud import secretmanager
import logging

class Config:
    # Initialize Secret Manager Client
    client = secretmanager.SecretManagerServiceClient()

    def get_secret(secret_name: str) -> str:
        project_id = os.getenv('GCP_PROJECT_ID')
        if not project_id:
            logging.error("GCP_PROJECT_ID is not set in environment variables.")
            raise EnvironmentError("GCP_PROJECT_ID is not set.")
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        try:
            response = Config.client.access_secret_version(request={"name": name})
            secret = response.payload.data.decode('UTF-8')
            return secret
        except Exception as e:
            logging.error(f"Failed to access secret {secret_name}: {str(e)}")
            raise e

    # Fetch secrets
    SECRET_KEY = get_secret("FLASK_SECRET_KEY")
    JWT_SECRET = get_secret("JWT_SECRET")
    API_KEY = get_secret("API_KEY")
    DATABASE_URL = get_secret("DATABASE_URL")

    # AWS S3
    AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME = get_secret("S3_BUCKET_NAME")
    S3_REGION = get_secret("S3_REGION")

    # AI Providers
    OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = get_secret("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

    # Celery
    CELERY_BROKER_URL = get_secret("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = get_secret("CELERY_RESULT_BACKEND")

    # Stripe
    STRIPE_API_KEY = get_secret("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET = get_secret("STRIPE_WEBHOOK_SECRET")

    # Chrome Web Store
    CHROME_WEBSTORE_CLIENT_ID = get_secret("CHROME_WEBSTORE_CLIENT_ID")
    CHROME_WEBSTORE_CLIENT_SECRET = get_secret("CHROME_WEBSTORE_CLIENT_SECRET")
    CHROME_WEBSTORE_REFRESH_TOKEN = get_secret("CHROME_WEBSTORE_REFRESH_TOKEN")
