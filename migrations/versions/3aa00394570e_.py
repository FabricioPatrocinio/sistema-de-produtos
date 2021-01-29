"""empty message

Revision ID: 3aa00394570e
Revises: 189fd1544749
Create Date: 2021-01-29 10:01:27.246397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa00394570e'
down_revision = '189fd1544749'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('img_perfil', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'img_perfil')
    # ### end Alembic commands ###
