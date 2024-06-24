"""add few columns on posts

Revision ID: 31acc7c139a7
Revises: 5313a0cec77a
Create Date: 2024-06-24 00:00:26.258804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31acc7c139a7'
down_revision: Union[str, None] = '5313a0cec77a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')
    ))
    
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
