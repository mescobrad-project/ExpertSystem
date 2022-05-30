"""Create WF and WFR tables

Revision ID: 04d665df5650
Revises: 
Create Date: 2022-05-30 13:56:30.406387

"""
from alembic import op
import sqlalchemy as sa
from src.models._base import GUID
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "04d665df5650"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "workflows",
        sa.Column("id", GUID(), primary_key=True, default=lambda: str(uuid4())),
        sa.Column("name", sa.String, nullable=False, unique=True, index=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("tasks", sa.JSON, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.sql.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.sql.func.now(),
            onupdate=sa.sql.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "runs",
        sa.Column("id", GUID(), primary_key=True, default=lambda: str(uuid4())),
        sa.Column(
            "workflow_id",
            GUID(),
            sa.ForeignKey("workflows.id", ondelete="RESTRICT", onupdate="CASCADE"),
        ),
        sa.Column("state", sa.JSON, nullable=True),
        sa.Column("steps", sa.JSON, nullable=True),
        sa.Column("queue", sa.JSON, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.sql.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.sql.func.now(),
            onupdate=sa.sql.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table("runs")
    op.drop_table("workflows")
