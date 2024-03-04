"""empty message

Revision ID: b01bd8a6e263
Revises: 8bce4f3cc18c
Create Date: 2024-02-12 06:37:09.834744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b01bd8a6e263'
down_revision = '8bce4f3cc18c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_last_login', sa.DateTime(), nullable=True))
        batch_op.drop_column('user_last_login')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_last_login', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('admin_last_login')

    # ### end Alembic commands ###