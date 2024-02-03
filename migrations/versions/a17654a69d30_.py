"""empty message

Revision ID: a17654a69d30
Revises: 29b69f735fc8
Create Date: 2024-01-30 18:54:44.607819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a17654a69d30'
down_revision = '29b69f735fc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('comment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment_report_id', sa.Integer(), nullable=True),
    sa.Column('comment_user_id', sa.Integer(), nullable=True),
    sa.Column('comment_desc', sa.Text(), nullable=False),
    sa.Column('comment_datetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['comment_report_id'], ['report.report_id'], ),
    sa.ForeignKeyConstraint(['comment_user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###