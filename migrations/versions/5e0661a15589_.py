"""empty message

Revision ID: 5e0661a15589
Revises: 2a71c0e2ebc1
Create Date: 2020-12-06 19:55:32.377843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e0661a15589'
down_revision = '2a71c0e2ebc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), server_default='0', nullable=False))
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.drop_column('users', 'active')
    # ### end Alembic commands ###