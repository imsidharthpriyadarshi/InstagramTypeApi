"""add email_otp table

Revision ID: c17eb40ba975
Revises: d93c4c86c07b
Create Date: 2022-05-31 21:52:45.880109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17eb40ba975'
down_revision = 'd93c4c86c07b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_verified',
               existing_type=sa.BOOLEAN(),
               )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_verified',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###