"""Removed conditions

Revision ID: 21cc9a522db4
Revises: 1dd075d3fd60
Create Date: 2014-11-15 00:52:04.059721

"""

# revision identifiers, used by Alembic.
revision = '21cc9a522db4'
down_revision = '1dd075d3fd60'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('arguments', sa.Text(), nullable=True),
    sa.Column('src_id', sa.Integer(), nullable=True),
    sa.Column('dst_id', sa.Integer(), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], [u'batches.id'], ),
    sa.ForeignKeyConstraint(['dst_id'], [u'scriptsteps.id'], ),
    sa.ForeignKeyConstraint(['src_id'], [u'scriptsteps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conditions')
    ### end Alembic commands ###
