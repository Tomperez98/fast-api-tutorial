"""add updated_at columns to posts table

Revision ID: 7458234d58ad
Revises: 
Create Date: 2021-12-05 20:18:02.807328

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7458234d58ad"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "test_table", sa.Column("id", sa.INTEGER, nullable=False, primary_key=True)
    )


def downgrade():
    op.drop_table("test_table")
