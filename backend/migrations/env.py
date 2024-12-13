# /backend/migrations/env.py
from __future__ import with_statement
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config import Config
from db import db

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

target_metadata = db.metadata

def run_migrations_offline():
    url = Config.SQLALCHEMY_DATABASE_URI
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle":"named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        connectable = db.engine
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()