"""author on posts

Revision ID: 12ca2a37c808
Revises: 7e974818ecdd
Create Date: 2023-06-08 20:02:46.562979

"""
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "12ca2a37c808"
down_revision = "7e974818ecdd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "post",
        sa.Column(
            "author_id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False
        ),
    )
    op.create_foreign_key(None, "post", "user", ["author_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "post", type_="foreignkey")
    op.drop_column("post", "author_id")
    # ### end Alembic commands ###
