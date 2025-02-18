import logging
import logging.config
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from db import db
from prometheus_metrics import setup_metrics
from routes.auth_routes import auth_bp
from routes.templates_routes import templates_bp
from routes.test_routes import test_bp
from routes.payments_routes import payments_bp  # Payments route registered here
from flasgger import Swagger
from flask_talisman import Talisman

# Setup structured logging with JSON formatting
logging.config.dictConfig({
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "formatters": {
        "default": {
            "format": '{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
        }
    },
    "root": {
        "handlers": ["default"],
        "level": "INFO"
    }
})

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# SECURITY: Set Content Security Policy (CSP) with a stricter policy.
csp = {
    'default-src': ["'self'"],
    # Allow only self-hosted styles and minimal inline styles (if absolutely necessary)
    'style-src': ["'self'"],
    # Block inline scripts to mitigate XSS
    'script-src': ["'self'"],
    'img-src': ["'self'", "data:"],
    'font-src': ["'self'"],
}
Talisman(app, content_security_policy=csp)

# RATE LIMITING: Prevent brute-force and DDoS attacks.
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"]
)

# API Documentation using Swagger
swagger = Swagger(app)

with app.app_context():
    db.create_all()

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(templates_bp, url_prefix='/templates')
app.register_blueprint(test_bp, url_prefix='/test')
app.register_blueprint(payments_bp, url_prefix='/payments')

# Setup Prometheus Metrics for monitoring API performance
setup_metrics(app)

# GLOBAL ERROR HANDLERS for 404 and 500 errors.
@app.errorhandler(404)
def not_found(e):
    # Log 404 errors for further analysis.
    app.logger.warning("404 Not Found: %s", e)
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    # Log the stack trace for debugging.
    app.logger.error("500 Internal Server Error: %s", e, exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # In production, use a WSGI server (like Gunicorn) instead of the built-in server.
    app.run(host='0.0.0.0', port=5000)
