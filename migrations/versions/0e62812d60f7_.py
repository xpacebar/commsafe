"""empty message

Revision ID: 0e62812d60f7
Revises: ceacbcf882a8
Create Date: 2024-01-22 20:09:12.792744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e62812d60f7'
down_revision = 'ceacbcf882a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_constraint('report_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('report_ibfk_3', type_='foreignkey')
        batch_op.drop_column('report_lga_id')
        batch_op.drop_column('report_state_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('report_state_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('report_lga_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('report_ibfk_3', 'state', ['report_state_id'], ['state_id'])
        batch_op.create_foreign_key('report_ibfk_2', 'lga', ['report_lga_id'], ['lga_id'])

    # ### end Alembic commands ###
