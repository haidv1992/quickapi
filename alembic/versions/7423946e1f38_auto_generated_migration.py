"""Auto-generated migration

Revision ID: 7423946e1f38
Revises: f9b2cbe1ab3d
Create Date: 2023-05-10 20:27:00.930045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7423946e1f38'
down_revision = 'f9b2cbe1ab3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_content', table_name='posts')
    op.drop_column('posts', 'content')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_posts_content', 'posts', ['content'], unique=False)
    # ### end Alembic commands ###
