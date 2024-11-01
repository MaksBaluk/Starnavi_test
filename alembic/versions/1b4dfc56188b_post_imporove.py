"""post imporove

Revision ID: 1b4dfc56188b
Revises: f5140f0613d9
Create Date: 2024-10-25 11:39:34.262568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b4dfc56188b'
down_revision: Union[str, None] = 'f5140f0613d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('auto_reply_delay', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'auto_reply_delay')
    # ### end Alembic commands ###
