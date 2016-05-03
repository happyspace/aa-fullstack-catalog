"""Item user relationship

Revision ID: f3fdfbabbade
Revises: bdcc67c48b91
Create Date: 2016-04-28 16:11:44.949835

"""

# revision identifiers, used by Alembic.
revision = 'f3fdfbabbade'
down_revision = 'bdcc67c48b91'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import delete, table, Column, Integer, Unicode
import sqlalchemy as sa



def upgrade():
    categories = table('category',
                       sa.Column('id', Integer, primary_key=True),
                       sa.Column('name', Unicode(50), nullable=False),
                       sa.Column('description', Unicode(200))
                       )

    op.bulk_insert(categories, [
        {'name': 'flowers', 'description': 'Flowering plants'},
        {'name': 'shrubs', 'description': 'Bushes'},
        {'name': 'trees', 'description': 'Trees'},
        {'name': 'vegetables', 'description': 'tomato, bean, beet, '
                                              'potato, onion, asparagus, '
                                              'spinach, cauliflower '
                                              'and many more'},
        {'name': 'grasses', 'description': 'herbaceous plants with jointed stems'}
    ])


def downgrade():
    conn = op.get_bind()

    res = conn.execute("delete from category")
