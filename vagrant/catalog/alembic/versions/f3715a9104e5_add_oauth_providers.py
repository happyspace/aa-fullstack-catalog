"""Add OAuth providers

Revision ID: f3715a9104e5
Revises: f3fdfbabbade
Create Date: 2016-05-03 11:35:27.586736

"""

# revision identifiers, used by Alembic.
revision = 'f3715a9104e5'
down_revision = 'f3fdfbabbade'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import delete, table, Column, Integer, Unicode

from alembic import op
import sqlalchemy as sa


def upgrade():
    providers = table('oa_provider',
                      sa.Column('id', Integer, primary_key=True),
                      sa.Column('name', Unicode(50), nullable=False),
                      sa.Column('description', Unicode(200))
                      )

    op.bulk_insert(providers, [
        {'name': 'google', 'description': 'OAuth 2 Google login'},
        {'name': 'facebook', 'description': 'OAuth 2 Facebook login'}
    ])


def downgrade():
    conn = op.get_bind()

    res = conn.execute("delete from oa_provider")

