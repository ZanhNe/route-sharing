"""delete noti_type column

Revision ID: b62f7c243d24
Revises: 0e3374afca88
Create Date: 2025-01-27 13:02:14.347520

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b62f7c243d24'
down_revision = '0e3374afca88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_column('noti_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('noti_type', mysql.ENUM('REQUEST', 'OTHER', collation='utf8mb4_unicode_ci'), nullable=False))

    # ### end Alembic commands ###
