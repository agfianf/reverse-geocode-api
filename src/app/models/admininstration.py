from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.helper.database_app import metadata


# Mendefinisikan tabel menggunakan pendekatan deklaratif
administration_boundaries = Table(
    "administration_boundaries",
    metadata,
    Column("srs_id", String(255)),
    Column("district", String(255)),
    Column("village", String(255)),
    Column("regency_city", String(255)),
    Column("province", String(255)),
    Column(
        "geom",
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=True),
    ),
    Column("country", String(255), nullable=True),
    Column("textsearchable_index_col", TSVECTOR),
)
