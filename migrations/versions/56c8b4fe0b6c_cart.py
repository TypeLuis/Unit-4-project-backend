"""Cart

Revision ID: 56c8b4fe0b6c
Revises: 304d7a5871ae
Create Date: 2023-03-23 15:07:25.732438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56c8b4fe0b6c'
down_revision = '304d7a5871ae'
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
