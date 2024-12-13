# /backend/prometheus_metrics.py
from prometheus_client import Counter, generate_latest
from flask import Response

req_counter = Counter('http_requests_total', 'Total HTTP Requests')

def setup_metrics(app):
    @app.before_request
    def before_request():
        req_counter.inc()

    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype='text/plain')
