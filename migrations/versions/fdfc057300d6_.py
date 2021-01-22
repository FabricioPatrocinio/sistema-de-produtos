"""empty message

Revision ID: fdfc057300d6
Revises: 32502e45b49d
Create Date: 2021-01-22 10:33:39.255942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdfc057300d6'
down_revision = '32502e45b49d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fabricante', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fabricante', 'users', ['user_id'], ['id'])
    op.add_column('referencia', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'referencia', 'users', ['user_id'], ['id'])
    op.add_column('tipo', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tipo', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tipo', type_='foreignkey')
    op.drop_column('tipo', 'user_id')
    op.drop_constraint(None, 'referencia', type_='foreignkey')
    op.drop_column('referencia', 'user_id')
    op.drop_constraint(None, 'fabricante', type_='foreignkey')
    op.drop_column('fabricante', 'user_id')
    # ### end Alembic commands ###