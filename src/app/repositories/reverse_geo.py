from fastapi import HTTPException, status
from geoalchemy2.functions import (
    ST_Contains,
    ST_Point,
)
from sqlalchemy import Select, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models.admininstration import administration_boundaries
from app.schemas.reverse_geo import AddressLocation, QueryParamsCoordinate


class ReverseGeocodeSQL:
    @staticmethod
    def get_contains_lat_long(
        payload: QueryParamsCoordinate,
    ) -> Select:
        return select(
            administration_boundaries.c.village,
            administration_boundaries.c.district,
            administration_boundaries.c.regency_city,
            administration_boundaries.c.province,
            administration_boundaries.c.country,
            administration_boundaries.c.geom,
        ).where(
            ST_Contains(
                administration_boundaries.c.geom,
                ST_Point(payload.lng, payload.lat, 4326),
            )
        )


class ReverseGeocodeRepositories:
    async def get_contains_lat_long(
        self, payload: QueryParamsCoordinate, connection: AsyncConnection
    ) -> AddressLocation:
        try:
            stmt = ReverseGeocodeSQL.get_contains_lat_long(payload)
            result = await connection.execute(stmt)
            result = result.one()
            return AddressLocation(
                sub_district=result.village,
                district=result.district,
                regency_city=result.regency_city,
                province=result.province,
                country=result.country,
            )
        except NoResultFound:
            raise HTTPException(  # noqa: B904
                status_code=status.HTTP_404_NOT_FOUND,
                detail="location not found",
            )
        except Exception as e:
            print(e.__class__)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error Exception for get contains lat long: {e}",
            ) from e
