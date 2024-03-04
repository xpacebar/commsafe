"""empty message

Revision ID: e11d85a68332
Revises: 6ac019f55163
Create Date: 2024-02-12 11:01:10.394488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e11d85a68332'
down_revision = '6ac019f55163'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('featured_services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('featured_email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('featured_date_created', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('featured_services', schema=None) as batch_op:
        batch_op.drop_column('featured_date_created')
        batch_op.drop_column('featured_email')

    # ### end Alembic commands ###
