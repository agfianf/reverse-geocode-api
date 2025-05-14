from sqlalchemy.ext.asyncio import AsyncConnection

from app.repositories.reverse_geo import ReverseGeocodeRepositories
from app.schemas.reverse_geo import (
    AddressLocation,
    QueryParamsCoordinate,
)


class ReverseGeocodeService:
    """Service for reverse geocoding latitude and longitude to address data."""

    def __init__(self, repo: ReverseGeocodeRepositories) -> None:
        self.repo = repo

    async def reverse_geocode(
        self,
        payload: QueryParamsCoordinate,
        connection: AsyncConnection,
    ) -> AddressLocation:
        result = await self.repo.get_contains_lat_long(
            payload=payload,
            connection=connection,
        )
        return result
