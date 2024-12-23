"""Add order column to RouteDetail table

Revision ID: f172a5518fd4
Revises: 4a3a46c93313
Create Date: 2024-12-05 00:00:35.020056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f172a5518fd4'
down_revision = '4a3a46c93313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routedetail', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routedetail', schema=None) as batch_op:
        batch_op.drop_column('order')

    # ### end Alembic commands ###
