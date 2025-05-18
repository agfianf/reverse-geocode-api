from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncConnection

from app.depedencies.database import get_async_conn
from app.depedencies.static_bearer import StaticBearer
from app.schemas.response_api import JsonResponse
from app.schemas.reverse_geo import AddressLocation, QueryParamsCoordinate
from app.services.reverse_geo import ReverseGeocodeService


router = APIRouter(
    prefix="/api/v1/satellite",
    tags=["Reverse Geocode"],
    dependencies=[Depends(StaticBearer())],
)


@router.get(
    "/reverse-geocode",
    name="Convert your latlong to address",
    response_model=JsonResponse[AddressLocation, None],
)
async def reverse_geocode(
    request: Request,
    payload: Annotated[QueryParamsCoordinate, Query()],
    connection: Annotated[AsyncConnection, Depends(get_async_conn)],
) -> JsonResponse[AddressLocation, None]:
    reverse_geocode_service: ReverseGeocodeService = request.state.reverse_geocode_service
    response = await reverse_geocode_service.reverse_geocode(
        payload=payload,
        connection=connection,
    )
    return JsonResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        data=response,
        message="Get Address Success",
    )
