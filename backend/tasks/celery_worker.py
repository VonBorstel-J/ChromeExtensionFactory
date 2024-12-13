from celery import Celery
from config import Config

celery = Celery('extension_factory', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def async_generate_code(user_idea, template_type, provider):
    # call generate_code_snippet and return result
    pass
