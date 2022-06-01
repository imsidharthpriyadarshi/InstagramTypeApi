"""add is_verified column in user

Revision ID: 1289c5069c59
Revises: c17eb40ba975
Create Date: 2022-05-31 22:05:01.217258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1289c5069c59'
down_revision = 'c17eb40ba975'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_verified',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_verified',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###