"""create-cart

Revision ID: 4dfa518a9580
Revises: 0f22f8b85685
Create Date: 2022-01-10 12:53:10.946292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4dfa518a9580"
down_revision = "0f22f8b85685"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "carts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("userId", sa.Integer),
        sa.Column("item_name", sa.String),
        sa.Column("item_price", sa.String),
        sa.Column("item_link", sa.String),
        sa.Column("item_img", sa.String),
        sa.Column("checkout_date", sa.String),
        sa.Column("checkedOut", sa.Boolean),
    )


def downgrade():
    op.drop_table("carts")
