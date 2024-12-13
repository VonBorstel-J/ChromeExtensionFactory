# /backend/tasks/celery_worker.py
from celery import Celery
from config import Config
from ai_service import generate_code_snippet

celery = Celery('extension_factory', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def async_generate_code(user_idea, template_type, provider):
    return generate_code_snippet(user_idea, template_type, provider)
