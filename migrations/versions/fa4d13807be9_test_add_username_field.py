"""test add username field

Revision ID: fa4d13807be9
Revises: 104a384df9fe
Create Date: 2023-11-28 14:07:17.701811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa4d13807be9'
down_revision: Union[str, None] = '104a384df9fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_table', sa.Column('username', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_table', 'username')
    # ### end Alembic commands ###
