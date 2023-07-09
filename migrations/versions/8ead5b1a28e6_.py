"""empty message

Revision ID: 8ead5b1a28e6
Revises: 
Create Date: 2023-07-09 12:22:58.804010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ead5b1a28e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('creditcards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('holder', sa.String(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('exp_date', sa.Date(), nullable=False),
    sa.Column('cvv', sa.String(), nullable=True),
    sa.Column('brand', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('creditcards')
    # ### end Alembic commands ###
