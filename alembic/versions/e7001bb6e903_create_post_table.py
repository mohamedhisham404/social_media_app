"""create post table

Revision ID: e7001bb6e903
Revises: 
Create Date: 2024-07-08 23:02:07.702856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7001bb6e903'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,print_only=True,primary_key=True),
                    sa.Column('title', sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
