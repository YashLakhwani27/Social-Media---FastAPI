"""Create Posts Table

Revision ID: 41af339010b7
Revises: 
Create Date: 2025-11-21 13:44:26.224173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41af339010b7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True) ,sa.Column("title",sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
    pass
