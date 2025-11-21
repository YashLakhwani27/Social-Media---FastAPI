"""Add foriegn key to posts table

Revision ID: ac8f342270b6
Revises: 45002850c03a
Create Date: 2025-11-21 14:39:51.263621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac8f342270b6'
down_revision: Union[str, Sequence[str], None] = '45002850c03a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fkey',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
