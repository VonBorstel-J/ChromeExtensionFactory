# /backend/prometheus_metrics.py
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from flask import Response, g, request
import time

req_counter = Counter('http_requests_total', 'Total HTTP Requests', ['endpoint', 'method', 'status'])
api_latency = Histogram('api_latency_seconds', 'Latency of API requests', ['endpoint', 'method'])
celery_tasks_total = Counter('celery_tasks_total', 'Total Celery Tasks', ['task_name', 'status'])
celery_tasks_in_progress = Gauge('celery_tasks_in_progress', 'Celery Tasks in Progress', ['task_name'])

def setup_metrics(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            latency = time.time() - g.start_time
            api_latency.labels(request.endpoint, request.method).observe(latency)
            req_counter.labels(request.endpoint, request.method, response.status_code).inc()
        return response

    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype='text/plain')
