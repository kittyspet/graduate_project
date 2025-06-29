"""revision

Revision ID: de5f86a226f4
Revises: c330afa21721
Create Date: 2024-12-26 15:16:44.965539

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa


revision = 'de5f86a226f4'
down_revision = 'c330afa21721'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'record_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('record_data', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
