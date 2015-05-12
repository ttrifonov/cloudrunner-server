"""Added Deployments

Revision ID: 26890f2dbb
Revises: 5700eeaec0ed
Create Date: 2015-05-08 17:04:56.572193

"""

# revision identifiers, used by Alembic.
revision = '26890f2dbb'
down_revision = '5700eeaec0ed'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('Pending', 'Started', 'Rebuilding', 'Patching', 'Stopped', 'Deleting', name='status'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], [u'users.id'], name=op.f('fk_deployments_owner_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_deployments')),
    sa.UniqueConstraint('name', 'owner_id', name=op.f('uq_deployments_name'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deployments')
    ### end Alembic commands ###