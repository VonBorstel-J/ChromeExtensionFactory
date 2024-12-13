# /backend/migrations/versions/20241213_initial.py
"""initial

Revision ID: 20241213_initial
Revises:
Create Date: 2024-12-13 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '20241213_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(128), nullable=False),
        sa.Column('is_premium', sa.Boolean, default=False)
    )

    op.create_table(
        'project',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('name', sa.String(200)),
        sa.Column('data', sa.JSON),
        sa.Column('created_at', sa.DateTime)
    )

    op.create_table(
        'template_rating',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('template_name', sa.String(200)),
        sa.Column('rating', sa.Integer)
    )

def downgrade():
    op.drop_table('template_rating')
    op.drop_table('project')
    op.drop_table('user')
