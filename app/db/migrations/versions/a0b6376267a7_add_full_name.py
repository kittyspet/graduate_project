"""add full_name

Revision ID: a0b6376267a7
Revises: 07fe03bd1c7f
Create Date: 2024-12-25 14:50:13.835208

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa


revision = 'a0b6376267a7'
down_revision = '07fe03bd1c7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column("full_name", sa.String))


def downgrade():
    pass
