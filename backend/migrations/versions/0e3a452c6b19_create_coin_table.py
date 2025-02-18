"""create coin table

Revision ID: 0e3a452c6b19
Revises: 4d003d2dcbd0
Create Date: 2025-02-03 01:50:18.766242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e3a452c6b19'
down_revision: Union[str, None] = '4d003d2dcbd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('last_price', sa.Float(), nullable=True),
    sa.Column('trend', sa.String(), nullable=True),
    sa.Column('change_percentage', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coins_id'), 'coins', ['id'], unique=False)
    op.create_index(op.f('ix_coins_name'), 'coins', ['name'], unique=False)
    op.create_index(op.f('ix_coins_symbol'), 'coins', ['symbol'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coins_symbol'), table_name='coins')
    op.drop_index(op.f('ix_coins_name'), table_name='coins')
    op.drop_index(op.f('ix_coins_id'), table_name='coins')
    op.drop_table('coins')
    # ### end Alembic commands ###
