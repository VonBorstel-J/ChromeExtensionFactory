# /backend/app.py
import logging
import logging.config
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from db import db
from prometheus_metrics import setup_metrics
from auth import token_required
from routes.auth_routes import auth_bp
from routes.templates_routes import templates_bp
from routes.test_routes import test_bp
from flasgger import Swagger
from flask_talisman import Talisman

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

# Security Headers
csp = {
    'default-src': [
        "'self'"
    ]
}
Talisman(app, content_security_policy=csp)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"]
)

# Swagger Documentation
swagger = Swagger(app)

with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(templates_bp, url_prefix='/templates')
app.register_blueprint(test_bp, url_prefix='/test')

# Setup Prometheus Metrics
setup_metrics(app)

# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
