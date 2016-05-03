"""Add applications table

Revision ID: 2fbedc64fcf4
Revises: f3715a9104e5
Create Date: 2016-05-03 14:10:14.858430

"""

# revision identifiers, used by Alembic.
revision = '2fbedc64fcf4'
down_revision = 'f3715a9104e5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.Column('app_id', sa.Unicode(length=250), nullable=False),
    sa.Column('app_secret', sa.Unicode(length=250), nullable=False),
    sa.Column('json', postgresql.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['oa_provider.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_id', 'app_id', name='application_provider_app_unique')
    )
    op.create_unique_constraint('oa_provider_name_unique', 'oa_provider', ['name'])
    op.drop_column('oa_provider', 'application_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oa_provider', sa.Column('application_id', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.drop_constraint('oa_provider_name_unique', 'oa_provider', type_='unique')
    op.drop_table('application')
    ### end Alembic commands ###
