from flask import Flask
from config import Config
from db import db
from prometheus_metrics import setup_metrics
from auth import token_required
from routes.auth_routes import auth_bp
from routes.templates_routes import templates_bp
# ... import other blueprints

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(templates_bp)
# ... register other blueprints

setup_metrics(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
