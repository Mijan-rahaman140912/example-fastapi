"""create posts table

Revision ID: 6b9ff88f8f72
Revises: 
Create Date: 2024-06-23 16:01:07.346300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b9ff88f8f72'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
