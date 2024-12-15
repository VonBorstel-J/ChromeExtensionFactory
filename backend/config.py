import os
import logging

class Config:
    @staticmethod
    def get_secret(secret_name: str, default_value: str = None) -> str:
        """
        Fetch secret from GCP Secret Manager. Return default value if GCP is not configured.
        """
        project_id = os.getenv('GCP_PROJECT_ID')
        if not project_id:
            logging.warning(f"GCP_PROJECT_ID is not set. Using default for {secret_name}.")
            return default_value

        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            response = client.access_secret_version(request={"name": name})
            secret = response.payload.data.decode('UTF-8')
            return secret
        except Exception as e:
            logging.warning(f"Failed to fetch secret {secret_name}: {str(e)}. Using default value.")
            return default_value

    # Fetch secrets with defaults for local development
    SECRET_KEY = get_secret("FLASK_SECRET_KEY", "default_flask_secret")
    JWT_SECRET = get_secret("JWT_SECRET", "default_jwt_secret")
    API_KEY = get_secret("API_KEY", "default_api_key")
    DATABASE_URL = get_secret("DATABASE_URL", "sqlite:///local.db")  # Fallback to SQLite for local dev

    # AWS S3
    AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY", None)
    S3_BUCKET_NAME = get_secret("S3_BUCKET_NAME", None)
    S3_REGION = get_secret("S3_REGION", None)

    # AI Providers
    OPENAI_API_KEY = get_secret("OPENAI_API_KEY", None)
    ANTHROPIC_API_KEY = get_secret("ANTHROPIC_API_KEY", None)
    GEMINI_API_KEY = get_secret("GEMINI_API_KEY", None)

    # Celery
    CELERY_BROKER_URL = get_secret("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = get_secret("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

    # Stripe
    STRIPE_API_KEY = get_secret("STRIPE_API_KEY", None)
    STRIPE_WEBHOOK_SECRET = get_secret("STRIPE_WEBHOOK_SECRET", None)

    # Chrome Web Store
    CHROME_WEBSTORE_CLIENT_ID = get_secret("CHROME_WEBSTORE_CLIENT_ID", None)
    CHROME_WEBSTORE_CLIENT_SECRET = get_secret("CHROME_WEBSTORE_CLIENT_SECRET", None)
    CHROME_WEBSTORE_REFRESH_TOKEN = get_secret("CHROME_WEBSTORE_REFRESH_TOKEN", None)
