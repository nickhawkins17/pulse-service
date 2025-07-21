"""create tracks table

Revision ID: 6eaebbe8abd4
Revises: 
Create Date: 2025-07-20 19:38:23.918796

"""
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eaebbe8abd4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tracks',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('track_name', sa.String, nullable=False),
        sa.Column('artist_names', ARRAY(sa.String), nullable=False),
        sa.Column('album_name', sa.String, nullable=True),
        sa.Column('track_id', sa.String, nullable=False, unique=True),
        sa.Column('uri', sa.String, nullable=False, unique=True),
        sa.Column('pulse_score', sa.Float, nullable=True),
    )

def downgrade():
    op.drop_table('tracks')
