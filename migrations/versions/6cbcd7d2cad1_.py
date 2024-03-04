"""empty message

Revision ID: 6cbcd7d2cad1
Revises: b01bd8a6e263
Create Date: 2024-02-12 10:37:57.168562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cbcd7d2cad1'
down_revision = 'b01bd8a6e263'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('featured_services',
    sa.Column('featured_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('featured_admin_id', sa.Integer(), nullable=True),
    sa.Column('featured_desc', sa.Text(), nullable=False),
    sa.Column('featured_address', sa.Text(), nullable=False),
    sa.Column('featured_img_file', sa.String(length=30), nullable=False),
    sa.Column('featured_phone', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['featured_admin_id'], ['admin.admin_id'], ),
    sa.PrimaryKeyConstraint('featured_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('featured_services')
    # ### end Alembic commands ###