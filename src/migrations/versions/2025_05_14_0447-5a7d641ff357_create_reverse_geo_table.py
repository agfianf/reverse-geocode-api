"""create reverse geo table

Revision ID: 5a7d641ff357
Revises: 
Create Date: 2025-05-14 04:47:29.230928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '5a7d641ff357'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # You need to makesure that postgis already installed on instance
    # you can check by using SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name LIKE 'postgis%';
    # if not please make request to your infra team to install postgis via package manager (apt/yum/apk/etc...)
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    op.create_table(
        "administration_boundaries",
        sa.Column('srs_id', sa.String(255)),
        sa.Column('district', sa.String(255)),
        sa.Column('village', sa.String(255)),
        sa.Column('regency_city', sa.String(255)),
        sa.Column('province', sa.String(255)),
        sa.Column('geom', geoalchemy2.types.Geometry(geometry_type="MULTIPOLYGON", srid=4326)),
        sa.Column('country', sa.String(255), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(table_name="administration_boundaries")
    op.execute("DROP EXTENSION IF EXISTS postgis;")
