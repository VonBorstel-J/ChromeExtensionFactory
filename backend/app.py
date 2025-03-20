import logging
import logging.config
import os
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from config import Config
from db import db
from prometheus_metrics import setup_metrics
from routes.auth_routes import auth_bp
from routes.templates_routes import templates_bp
from routes.test_routes import test_bp
from routes.payments_routes import payments_bp
from flasgger import Swagger
from flask_talisman import Talisman
from werkzeug.exceptions import HTTPException
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from datetime import datetime

# Initialize Sentry for error tracking
if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment=os.getenv('FLASK_ENV', 'development')
    )

# Setup structured logging with JSON formatting
logging.config.dictConfig({
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "default"
        }
    },
    "formatters": {
        "default": {
            "format": '{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s","module":"%(module)s","function":"%(funcName)s","line":%(lineno)d}'
        }
    },
    "root": {
        "handlers": ["default", "file"],
        "level": os.getenv('LOG_LEVEL', 'INFO')
    }
})

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, 
    resources={r"/*": {
        "origins": os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(','),
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-CSRF-Token"],
        "supports_credentials": True,
        "max_age": 3600
    }},
    supports_credentials=True
)

# Database configuration with connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
    'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
    'pool_pre_ping': True,
    'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
    'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 5))
}

db.init_app(app)

# SECURITY: Set Content Security Policy (CSP) with a stricter policy.
csp = {
    'default-src': ["'self'"],
    'style-src': ["'self'", "'unsafe-inline'"],
    'script-src': ["'self'"],
    'img-src': ["'self'", "data:", "https:"],
    'font-src': ["'self'", "https:", "data:"],
    'connect-src': ["'self'", "https://api.stripe.com"],
    'frame-ancestors': ["'none'"],
    'form-action': ["'self'"],
    'base-uri': ["'self'"],
    'object-src': ["'none'"],
    'media-src': ["'self'"],
    'frame-src': ["'none'"],
    'worker-src': ["'self'"],
    'manifest-src': ["'self'"],
    'upgrade-insecure-requests': []
}

Talisman(app, 
    content_security_policy=csp,
    force_https=os.getenv('FLASK_ENV') == 'production',
    strict_transport_security=True,
    session_cookie_secure=True,
    session_cookie_http_only=True,
    session_cookie_samesite='Lax'
)

# RATE LIMITING: Prevent brute-force and DDoS attacks.
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"],
    storage_uri=os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')
)

# API Documentation using Swagger
swagger = Swagger(app, 
    template={
        "swagger": "2.0",
        "info": {
            "title": "Chrome Extension Factory API",
            "description": "API for Chrome Extension Factory",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    }
)

with app.app_context():
    db.create_all()

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(templates_bp, url_prefix='/templates')
app.register_blueprint(test_bp, url_prefix='/test')
app.register_blueprint(payments_bp, url_prefix='/payments')

# Setup Prometheus Metrics for monitoring API performance
setup_metrics(app)

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = 'unhealthy'

    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# GLOBAL ERROR HANDLERS
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Handle all HTTP exceptions."""
    logger.warning(f"HTTP {e.code}: {e.name} - {e.description}")
    return jsonify({
        "error": e.name,
        "message": e.description,
        "code": e.code
    }), e.code

@app.errorhandler(Exception)
def handle_generic_exception(e):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "code": 500
    }), 500

@app.before_request
def before_request():
    """Log all incoming requests."""
    logger.info(f"Incoming request: {request.method} {request.url}")

@app.after_request
def after_request(response):
    """Log all outgoing responses."""
    logger.info(f"Outgoing response: {response.status}")
    return response

if __name__ == '__main__':
    # In production, use a WSGI server (like Gunicorn) instead of the built-in server.
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
