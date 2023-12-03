"""create index_status_location_company_department_position_on_employees

Revision ID: 7f3c61baa633
Revises: 8247b089361b
Create Date: 2023-11-30 18:50:39.776264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from itertools import combinations

# revision identifiers, used by Alembic.
revision: str = '7f3c61baa633'
down_revision: Union[str, None] = '8247b089361b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    try:
        op.execute('COMMIT')
    except:
        pass
    cols = ["status", "location", "company", "department", "position"]
    for i_size in range(len(cols)):
        for i_cols in combinations(cols, i_size + 1):
            new_cols = (*i_cols, 'organization')
            new_short_cols = [col[:3] for col in new_cols] 
            op.create_index(
                f"index_{'_'.join(new_short_cols)}_on_employees",
                "employees",
                new_cols,
                postgresql_concurrently=True
            )

def downgrade() -> None:
    cols = ["status", "location", "company", "department", "position"]
    for i_size in range(len(cols)):
        for i_cols in combinations(cols, i_size + 1):
            new_cols = (*i_cols, 'organization')
            new_short_cols = [col[:3] for col in new_cols] 
            op.drop_index(
                f"index_{'_'.join(new_short_cols)}_on_employees",
                "employees"
            )
