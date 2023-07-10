"""Creates key AES to encrypt credit card number

Revision ID: 62ed2814d5fd
Revises: 8ead5b1a28e6
Create Date: 2023-07-09 23:25:45.876134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62ed2814d5fd"
down_revision = "8ead5b1a28e6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("creditcards", schema=None) as batch_op:
        batch_op.add_column(sa.Column("key", sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("creditcards", schema=None) as batch_op:
        batch_op.drop_column("key")

    # ### end Alembic commands ###
