"""empty message

Revision ID: 0936d0f53506
Revises: 
Create Date: 2020-12-04 22:51:23.432525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0936d0f53506'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contracts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contract_type', sa.String(length=100), nullable=True),
    sa.Column('market', sa.Enum('BITCOIN', 'ETHEREUM', name='ticker'), nullable=True),
    sa.Column('size', sa.Float(), nullable=True),
    sa.Column('date_open', sa.DateTime(), nullable=True),
    sa.Column('date_close', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('trade_result', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contracts')
    # ### end Alembic commands ###
