"""empty message

Revision ID: 8bce4f3cc18c
Revises: ecc8ebe41424
Create Date: 2024-02-11 14:42:41.928268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bce4f3cc18c'
down_revision = 'ecc8ebe41424'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_fname', sa.String(length=30), nullable=True),
    sa.Column('admin_lname', sa.String(length=30), nullable=True),
    sa.Column('admin_email', sa.String(length=120), nullable=False),
    sa.Column('admin_pwd', sa.String(length=255), nullable=False),
    sa.Column('admin_gender', sa.Enum('male', 'female'), nullable=True),
    sa.Column('admin_type', sa.Enum('super admin', 'regular'), nullable=True),
    sa.Column('admin_date_created', sa.DateTime(), nullable=True),
    sa.Column('user_last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('admin_id'),
    sa.UniqueConstraint('admin_email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin')
    # ### end Alembic commands ###