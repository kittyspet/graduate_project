"""add full_name

Revision ID: 07fe03bd1c7f
Revises: 08036ffeaba4
Create Date: 2024-12-25 14:46:59.835758

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa


revision = '07fe03bd1c7f'
down_revision = '08036ffeaba4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column("full_name", sa.String))
    pass


def downgrade():
    pass
