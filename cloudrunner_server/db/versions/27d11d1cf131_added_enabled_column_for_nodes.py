"""Added enabled column for nodes

Revision ID: 27d11d1cf131
Revises: 5ac452375150
Create Date: 2015-02-04 17:55:22.152450

"""

# revision identifiers, used by Alembic.
revision = '27d11d1cf131'
down_revision = '5ac452375150'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nodes', sa.Column('enabled', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nodes', 'enabled')
    ### end Alembic commands ###
