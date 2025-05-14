"""adding foreing-key for post t

Revision ID: 7faa4cc54acb
Revises: eac515e32d81
Create Date: 2025-05-13 18:20:22.539283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7faa4cc54acb'
down_revision: Union[str, None] = 'eac515e32d81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'],
                          remote_cols=['id'], ondelete="CASCADE")

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
