"""add columns in posts table

Revision ID: aceaa664d3f7
Revises: 42d5b4d61eef
Create Date: 2024-07-09 00:00:26.515067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aceaa664d3f7'
down_revision: Union[str, None] = '42d5b4d61eef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(),nullable=False,server_default='TRUE')
    )
    op.add_column('posts',sa.Column(
        'votes',sa.Integer(),nullable=False,server_default='0')
    )
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('NOW()'))
    )


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','votes')
    op.drop_column('posts','created_at')
