"""create-user

Revision ID: 0f22f8b85685
Revises: 
Create Date: 2022-01-10 11:12:15.368907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0f22f8b85685"
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
