"""Added deployment resources

Revision ID: 2610fe726b06
Revises: 108f85f77ecb
Create Date: 2015-05-22 14:27:41.664046

"""

# revision identifiers, used by Alembic.
revision = '2610fe726b06'
down_revision = '108f85f77ecb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('depl_resources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server_name', sa.String(length=255), nullable=True),
    sa.Column('server_id', sa.String(length=255), nullable=True),
    sa.Column('meta', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deployment_id'], [u'deployments.id'], name=op.f('fk_depl_resources_deployment_id_deployments')),
    sa.ForeignKeyConstraint(['profile_id'], [u'cloud_profiles.id'], name=op.f('fk_depl_resources_profile_id_cloud_profiles')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_depl_resources')),
    sa.UniqueConstraint('server_id', 'profile_id', name=op.f('uq_depl_resources_server_id'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('depl_resources')
    ### end Alembic commands ###
