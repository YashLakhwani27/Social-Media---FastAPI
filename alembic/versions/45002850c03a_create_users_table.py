"""Create users table

Revision ID: 45002850c03a
Revises: fef9406b7930
Create Date: 2025-11-21 14:33:08.744376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45002850c03a'
down_revision: Union[str, Sequence[str], None] = 'fef9406b7930'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_table('users',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                   sa.Column('email',sa.String(),nullable=False),
                   sa.Column('password',sa.Integer(),nullable=False),
                   sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                   sa.UniqueConstraint('email'))
    

def downgrade() -> None:
    op.drop_table('users')
    pass
