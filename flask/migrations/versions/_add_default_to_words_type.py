"""add type to words

Revision ID: bc4c0e777557
Revises: bc4c0e777556
Create Date: 2023-09-11 19:20:55.035020

"""
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'bc4c0e777557'
down_revision = 'bc4c0e777556'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE words
            SET type = 0
            WHERE type IS NULL
            """
        )
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE words
            SET type = NULL
            WHERE type IS NOT NULL
            """
        )
    )
