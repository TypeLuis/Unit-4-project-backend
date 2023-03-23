"""User

Revision ID: 304d7a5871ae
Revises: 
Create Date: 2023-03-23 15:06:33.693016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304d7a5871ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String),
    )


def downgrade():
    op.drop_table("users")
