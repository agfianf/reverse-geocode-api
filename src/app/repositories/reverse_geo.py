from fastapi import HTTPException, status
from geoalchemy2.functions import (
    ST_Contains,
    ST_Point,
)
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admininstration import administration_boundaries
from app.schemas.reverse_geo import QueryParamsCoordinate


class ReverseGeocodeRepositories:
    async def get_contains_lat_long(
        self, payload: QueryParamsCoordinate, session: AsyncSession
    ):
        try:
            stmt = select(
                administration_boundaries.c.village,
                administration_boundaries.c.district,
                administration_boundaries.c.regency_city,
                administration_boundaries.c.province,
                administration_boundaries.c.country,
                administration_boundaries.c.geom,
            ).where(
                ST_Contains(
                    administration_boundaries.c.geom,
                    ST_Point(payload.longitude, payload.latitude, 4326),
                )
            )
            result = await session.execute(stmt)
            return result.one()
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
