import json

from sqlalchemy.ext.asyncio import AsyncConnection

from app.integrations.redis import RedisHelper
from app.repositories.reverse_geo import ReverseGeocodeRepositories
from app.schemas.reverse_geo import (
    AddressLocation,
    QueryParamsCoordinate,
)


class ReverseGeocodeService:
    """Service for reverse geocoding latitude and longitude to address data."""

    def __init__(self, repo: ReverseGeocodeRepositories, cache: RedisHelper) -> None:
        self.repo = repo
        self.cache = cache

    async def reverse_geocode(
        self,
        payload: QueryParamsCoordinate,
        connection: AsyncConnection,
    ) -> AddressLocation:
        cache_key = f"reverse_geo:{payload.lat}:{payload.lng}"
        cached = self.cache.get_data(cache_key)
        if cached:
            data = json.loads(cached)
            return AddressLocation(**data)

        result = await self.repo.get_contains_lat_long(
            payload=payload,
            connection=connection,
        )

        # Cache the result for 1 hour (3600 seconds)
        self.cache.set_data(cache_key, json.dumps(result.model_dump()), expire_sec=3600)
        return result
