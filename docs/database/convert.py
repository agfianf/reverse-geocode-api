import geopandas as gpd

from geoalchemy2 import Geometry
from shapely import wkt
from shapely.geometry import MultiPolygon
from sqlalchemy import create_engine


# Create a SQLAlchemy engine to connect to the PostGIS-enabled PostgreSQL database
engine = create_engine("postgresql+psycopg://user:password@localhost:5432/database_geo")

# Read the shapefile containing administrative boundaries
gdf = gpd.read_file("Batas_Wilayah_KelurahanDesa_10K_AR.shp")

# Select and rename only the relevant columns for the database schema
selected_columns = {
    "SRS_ID": "srs_id",  # Spatial Reference System Identifier
    "WADMKC": "district",  # District/Kecamatan name
    "WADMKD": "village",  # Village/Desa name
    "WADMKK": "regency_city",  # Regency/City (Kabupaten/Kota) name
    "WADMPR": "province",  # Province name
    "geometry": "geom",  # Geometry column
}
gdf = gdf[list(selected_columns.keys())].rename(columns=selected_columns)

# Add a static column for country, since it's not present in the shapefile
gdf["country"] = "Indonesia"

# Display the first few rows for inspection (optional)
gdf.head()

# Ensure the geometry column is set and convert all geometries to EPSG:4326 (WGS84)
gdf = gdf.set_geometry("geom")
gdf = gdf.to_crs(epsg=4326)


# Function to convert any geometry to a valid 2D MULTIPOLYGON
def to_multipolygon_2d(geom):
    if geom is None or geom.is_empty:
        return None
    # Fix invalid geometries if necessary
    if not geom.is_valid:
        geom = geom.buffer(0)
    # Remove Z dimension (if present) by dumping to WKT and reloading as 2D
    wkt_2d = wkt.dumps(geom, output_dimension=2)
    geom_2d = wkt.loads(wkt_2d)
    # Convert to MultiPolygon if needed
    if geom_2d.geom_type == "Polygon":
        return MultiPolygon([geom_2d])
    if geom_2d.geom_type == "MultiPolygon":
        return geom_2d
    # Return None for unsupported geometry types
    return None


# Apply the conversion to all geometries in the GeoDataFrame
gdf["geom"] = gdf["geom"].apply(to_multipolygon_2d)

# Remove any rows with missing or invalid geometries
gdf = gdf.dropna(subset=["geom"])

# Display the first few rows after geometry processing (optional)
gdf.head()

# Write the processed GeoDataFrame to the PostGIS database
gdf.to_postgis(
    name="administration_boundaries",
    con=engine,
    if_exists="append",  # Use 'replace' to overwrite the table if needed
    schema="public",
    index=False,
    chunksize=10000,
    dtype={"geom": Geometry("MULTIPOLYGON", srid=4326)},
)

print("Data successfully inserted into PostGIS!")
