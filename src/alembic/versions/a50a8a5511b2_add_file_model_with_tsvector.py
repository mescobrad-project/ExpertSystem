"""Add File Model with TSVector.

Revision ID: a50a8a5511b2
Revises: d721fd138a69
Create Date: 2023-01-18 18:19:49.128679

"""
from alembic import op
from src.models._base import GUID
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a50a8a5511b2"
down_revision = "d721fd138a69"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "files",
        sa.Column("user_id", GUID(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("bucket_name", sa.String(), nullable=True),
        sa.Column("object_name", sa.String(), nullable=True),
        sa.Column("id", GUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["expert_system.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="expert_system",
    )
    op.create_index(
        op.f("ix_expert_system_files_user_id"),
        "files",
        ["user_id"],
        unique=False,
        schema="expert_system",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_expert_system_files_user_id"),
        table_name="files",
        schema="expert_system",
    )
    op.drop_table("files", schema="expert_system")
    # ### end Alembic commands ###