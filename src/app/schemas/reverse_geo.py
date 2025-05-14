from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude


class QueryParamsCoordinate(BaseModel):
    latitude: Latitude = Field(
        ...,
        description="Google Satellite Latitude (EPSG:4326)",
    )
    longitude: Longitude = Field(
        ...,
        description="Google Satellite Longitude (EPSG:4326)",
    )


class AddressLocation(BaseModel):
    sub_district: str | None = Field(
        None, description="Sub-district or village of the address."
    )
    district: str | None = Field(None, description="District of the address.")
    regency_city: str | None = Field(None, description="Regency or city of the address.")
    province: str | None = Field(None, description="Province of the address.")
    country: str | None = Field(None, description="Country of the address.")
