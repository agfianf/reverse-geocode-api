from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.reverse_geo import ReverseGeocodeRepositories
from app.schemas.common import (
    AddressLocation,
    GetContainsLatLong,
)
from app.schemas.reverse_geo import QueryParamsCoordinate


class ReverseGeocodeService:
    """Service for reverse geocoding latitude and longitude to address data."""

    def __init__(self, repo: ReverseGeocodeRepositories) -> None:
        self.repo = repo

    async def reverse_geocode(
        self,
        payload: QueryParamsCoordinate,
        session: AsyncSession,
    ) -> AddressLocation:
        result = await self.repo.get_contains_lat_long(
            payload=payload,
            session=session,
        )
        return AddressLocation(
            sub_district=result.village,
            district=result.district,
            regency_city=result.regency_city,
            province=result.province,
            country=result.country,
        )
