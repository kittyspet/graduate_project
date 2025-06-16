"""create account table

Revision ID: 92afe75c21dd
Revises: d6e3a38b1fbd
Create Date: 2024-12-25 14:15:00.541107

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa


revision = '92afe75c21dd'
down_revision = 'd6e3a38b1fbd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
    )
    pass


def downgrade():
    pass
