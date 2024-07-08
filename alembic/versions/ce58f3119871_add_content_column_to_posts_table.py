"""add content column to posts table

Revision ID: ce58f3119871
Revises: e7001bb6e903
Create Date: 2024-07-08 23:09:07.178262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce58f3119871'
down_revision: Union[str, None] = 'e7001bb6e903'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column('posts',"content")
