"""delete username

Revision ID: 104a384df9fe
Revises: 8601d06e7e88
Create Date: 2023-11-14 12:39:13.355268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '104a384df9fe'
down_revision: Union[str, None] = '8601d06e7e88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_table_username_key', 'user_table', type_='unique')
    op.drop_column('user_table', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_table', sa.Column('username', sa.VARCHAR(length=99), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_table_username_key', 'user_table', ['username'])
    # ### end Alembic commands ###