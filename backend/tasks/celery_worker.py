# /backend/tasks/celery_worker.py
from celery import Celery
from config import Config
from ai_service import generate_code_snippet
from prometheus_client import Counter, Gauge
import logging

celery = Celery('extension_factory', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

celery_tasks_total = Counter('celery_tasks_total', 'Total Celery Tasks', ['task_name', 'status'])
celery_tasks_in_progress = Gauge('celery_tasks_in_progress', 'Celery Tasks in Progress', ['task_name'])

@celery.task(bind=True)
def async_generate_code(self, user_idea, template_type, provider):
    task_name = self.name
    celery_tasks_total.labels(task_name, 'started').inc()
    celery_tasks_in_progress.labels(task_name).inc()
    try:
        code = generate_code_snippet(user_idea, template_type, provider)
        celery_tasks_total.labels(task_name, 'success').inc()
        return {"status": "success", "code": code}
    except Exception as e:
        logging.error(f"Celery task {task_name} failed: {str(e)}")
        celery_tasks_total.labels(task_name, 'failure').inc()
        return {"status": "failure", "error": str(e)}
    finally:
        celery_tasks_in_progress.labels(task_name).dec()
