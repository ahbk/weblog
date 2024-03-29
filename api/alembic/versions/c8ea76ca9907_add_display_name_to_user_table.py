"""add display_name to user table

Revision ID: c8ea76ca9907
Revises: 12ca2a37c808
Create Date: 2023-06-11 21:14:55.130717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c8ea76ca9907"
down_revision = "12ca2a37c808"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("display_name", sa.String(length=30), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "display_name")
    # ### end Alembic commands ###
