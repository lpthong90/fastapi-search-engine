"""create employees table

Revision ID: 8247b089361b
Revises: 
Create Date: 2023-11-29 23:09:06.521432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8247b089361b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('contact_info', sa.String(), nullable=False),
        sa.Column('organization', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('position', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('employees')
