"""Added phone field for User

Revision ID: 330568e8928c
Revises: 1231d6a65b06
Create Date: 2015-02-05 16:53:40.517660

"""

# revision identifiers, used by Alembic.
revision = '330568e8928c'
down_revision = '1231d6a65b06'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    ### end Alembic commands ###
