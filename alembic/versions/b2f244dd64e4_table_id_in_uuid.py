"""table id in uuid

Revision ID: b2f244dd64e4
Revises: 54e79a06374c
Create Date: 2022-06-05 13:34:43.477608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2f244dd64e4'
down_revision = '54e79a06374c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_comment_id', table_name='comment')
    op.drop_index('ix_post_pic_id', table_name='post_pic')
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_index('ix_users_id', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_posts_id', 'posts', ['id'], unique=False)
    op.create_index('ix_post_pic_id', 'post_pic', ['id'], unique=False)
    op.create_index('ix_comment_id', 'comment', ['id'], unique=False)
    # ### end Alembic commands ###