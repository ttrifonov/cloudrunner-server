"""Removed conditions

Revision ID: 1dd075d3fd60
Revises: 502527a432a2
Create Date: 2014-11-15 00:51:44.210440

"""

# revision identifiers, used by Alembic.
revision = '1dd075d3fd60'
down_revision = '502527a432a2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conditions')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conditions',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('type', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('arguments', mysql.TEXT(), nullable=True),
    sa.Column('source_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('dest_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('batch_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], [u'batches.id'], name=u'conditions_ibfk_1'),
    sa.ForeignKeyConstraint(['dest_id'], [u'scripts.id'], name=u'conditions_ibfk_2'),
    sa.ForeignKeyConstraint(['source_id'], [u'scripts.id'], name=u'conditions_ibfk_3'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
