"""add device_id to images

Revision ID: a36d9e3766e3
Revises: 60fdc74ef914
Create Date: 2026-07-10 06:32:55.887681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a36d9e3766e3'
down_revision: Union[str, Sequence[str], None] = '60fdc74ef914'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "images",
        sa.Column("device_id", sa.Integer(), nullable=False),
    )

    op.create_foreign_key(
        "images_device_id_fkey",
        "images",
        "devices",
        ["device_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "images_device_id_fkey",
        "images",
        type_="foreignkey",
    )

    op.drop_column("images", "device_id")