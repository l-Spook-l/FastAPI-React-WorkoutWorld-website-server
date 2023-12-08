"""initial

Revision ID: 8e29a778be97
Revises: 
Create Date: 2023-11-03 16:37:01.665473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e29a778be97'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('difficulty_workout_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_difficulty_workout_table_id'), 'difficulty_workout_table', ['id'], unique=True)
    op.create_table('role_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=99), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_table_id'), 'role_table', ['id'], unique=True)
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=99), nullable=False),
    sa.Column('last_name', sa.String(length=99), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=99), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_table_id'), 'user_table', ['id'], unique=True)
    op.create_table('workout_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('difficulty_id', sa.Integer(), nullable=False),
    sa.Column('total_time', sa.String(length=999), nullable=False),
    sa.ForeignKeyConstraint(['difficulty_id'], ['difficulty_workout_table.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workout_table_id'), 'workout_table', ['id'], unique=True)
    op.create_table('added_workouts_association',
    sa.Column('workout_table', sa.Integer(), nullable=True),
    sa.Column('user_table', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_table'], ['user_table.id'], ),
    sa.ForeignKeyConstraint(['workout_table'], ['workout_table.id'], )
    )
    op.create_table('exercise_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('number_of_sets', sa.Integer(), nullable=False),
    sa.Column('maximum_repetitions', sa.Integer(), nullable=False),
    sa.Column('rest_time', sa.Integer(), nullable=True),
    sa.Column('video', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['workout_id'], ['workout_table.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_table_id'), 'exercise_table', ['id'], unique=True)
    op.create_table('exercise_photo_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('photo', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise_table.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_photo_table_id'), 'exercise_photo_table', ['id'], unique=True)
    op.create_table('set_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('repetition', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise_table.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_set_table_id'), 'set_table', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_set_table_id'), table_name='set_table')
    op.drop_table('set_table')
    op.drop_index(op.f('ix_exercise_photo_table_id'), table_name='exercise_photo_table')
    op.drop_table('exercise_photo_table')
    op.drop_index(op.f('ix_exercise_table_id'), table_name='exercise_table')
    op.drop_table('exercise_table')
    op.drop_table('added_workouts_association')
    op.drop_index(op.f('ix_workout_table_id'), table_name='workout_table')
    op.drop_table('workout_table')
    op.drop_index(op.f('ix_user_table_id'), table_name='user_table')
    op.drop_table('user_table')
    op.drop_index(op.f('ix_role_table_id'), table_name='role_table')
    op.drop_table('role_table')
    op.drop_index(op.f('ix_difficulty_workout_table_id'), table_name='difficulty_workout_table')
    op.drop_table('difficulty_workout_table')
    # ### end Alembic commands ###