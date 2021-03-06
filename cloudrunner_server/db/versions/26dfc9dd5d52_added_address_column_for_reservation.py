"""Added 'address' column for Reservation

Revision ID: 26dfc9dd5d52
Revises: 24b5de6bb949
Create Date: 2015-02-19 16:04:08.933392

"""

# revision identifiers, used by Alembic.
revision = '26dfc9dd5d52'
down_revision = '24b5de6bb949'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nodereservations', sa.Column('address', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nodereservations', 'address')
    ### end Alembic commands ###
