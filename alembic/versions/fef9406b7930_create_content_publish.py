"""Create content publish

Revision ID: fef9406b7930
Revises: 41af339010b7
Create Date: 2025-11-21 14:22:30.805447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fef9406b7930'
down_revision: Union[str, Sequence[str], None] = '41af339010b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    op.add_column('posts',sa.Column('published',sa.Boolean(), default=True,nullable=False))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
