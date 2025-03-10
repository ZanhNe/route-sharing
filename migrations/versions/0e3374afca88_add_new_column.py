"""add new column

Revision ID: 0e3374afca88
Revises: 1ed00f440e9a
Create Date: 2025-01-17 10:01:00.734014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e3374afca88'
down_revision = '1ed00f440e9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roadmap_pairing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))

    with op.batch_alter_table('roadmap_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('date')

    with op.batch_alter_table('roadmap_share', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))

    with op.batch_alter_table('schedule_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('date')

    with op.batch_alter_table('schedule_pairing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))

    with op.batch_alter_table('schedule_pairing_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('date')

    with op.batch_alter_table('schedule_share', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedule_share', schema=None) as batch_op:
        batch_op.drop_column('created_date')

    with op.batch_alter_table('schedule_pairing_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', mysql.DATETIME(), nullable=False))
        batch_op.drop_column('created_date')

    with op.batch_alter_table('schedule_pairing', schema=None) as batch_op:
        batch_op.drop_column('created_date')

    with op.batch_alter_table('schedule_management', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', mysql.DATETIME(), nullable=False))
        batch_op.drop_column('created_date')

    with op.batch_alter_table('roadmap_share', schema=None) as batch_op:
        batch_op.drop_column('created_date')

    with op.batch_alter_table('roadmap_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', mysql.DATETIME(), nullable=False))
        batch_op.drop_column('created_date')

    with op.batch_alter_table('roadmap_pairing', schema=None) as batch_op:
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###
