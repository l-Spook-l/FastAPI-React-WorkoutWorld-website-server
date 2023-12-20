"""number in workout for exrcise

Revision ID: 476aa5bf8377
Revises: fa4d13807be9
Create Date: 2023-12-20 13:07:50.762735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '476aa5bf8377'
down_revision: Union[str, None] = 'fa4d13807be9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise_table', sa.Column('number_in_workout', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercise_table', 'number_in_workout')
    # ### end Alembic commands ###
