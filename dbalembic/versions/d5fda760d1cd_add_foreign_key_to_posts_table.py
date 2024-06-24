"""add foreign-key to posts table

Revision ID: d5fda760d1cd
Revises: 85ec6c1dc396
Create Date: 2024-06-23 23:05:32.785146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5fda760d1cd'
down_revision: Union[str, None] = '85ec6c1dc396'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE")
    
    pass


def downgrade():
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
