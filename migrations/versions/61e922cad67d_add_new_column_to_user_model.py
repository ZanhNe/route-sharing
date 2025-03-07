"""Add new column to user model

Revision ID: 61e922cad67d
Revises: b895367a8918
Create Date: 2025-02-18 16:53:05.474773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e922cad67d'
down_revision = 'b895367a8918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roadmap_pairing_request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'DECLINED', 'CANCELLED', 'FREE', name='status'), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('roadmap_pairing_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['roadmap_pairing_id'], ['roadmap_pairing.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('schedulepairing_roadmappairing', schema=None) as batch_op:
        batch_op.drop_constraint('schedulepairing_roadmappairing_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('schedulepairing_roadmappairing_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'roadmap_pairing', ['roadmap_pairing_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'schedule_pairing', ['schedule_pairing_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_verified')

    with op.batch_alter_table('schedulepairing_roadmappairing', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('schedulepairing_roadmappairing_ibfk_1', 'roadmap_pairing', ['roadmap_pairing_id'], ['id'])
        batch_op.create_foreign_key('schedulepairing_roadmappairing_ibfk_2', 'schedule_pairing', ['schedule_pairing_id'], ['id'])

    op.drop_table('roadmap_pairing_request')
    # ### end Alembic commands ###
