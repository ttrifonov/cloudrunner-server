"""Added Batches, added allow_sudo on script, added NodeTags

Revision ID: 438821cb5fb5
Revises: cbd5e53d894
Create Date: 2014-11-14 16:31:16.477037

"""

# revision identifiers, used by Alembic.
revision = '438821cb5fb5'
down_revision = 'cbd5e53d894'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('private', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nodetags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], [u'nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('script2batch',
    sa.Column('script_id', sa.Integer(), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ),
    sa.ForeignKeyConstraint(['script_id'], ['scripts.id'], )
    )
    op.create_table('conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('arguments', sa.Text(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('dest_id', sa.Integer(), nullable=True),
    sa.Column('src_version', sa.String(length=40), nullable=True),
    sa.Column('dst_version', sa.String(length=40), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], [u'batches.id'], ),
    sa.ForeignKeyConstraint(['dest_id'], [u'scripts.id'], ),
    sa.ForeignKeyConstraint(['source_id'], [u'scripts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'scripts', sa.Column('allow_sudo', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'scripts', 'allow_sudo')
    op.drop_table('conditions')
    op.drop_table('script2batch')
    op.drop_table('nodetags')
    op.drop_table('batches')
    ### end Alembic commands ###