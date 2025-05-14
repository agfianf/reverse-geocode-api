from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.depedencies.static_bearer import StaticBearer
from app.schemas.response_api import JsonResponse
from app.schemas.reverse_geo import QueryParamsCoordinate
from app.services.reverse_geo import ReverseGeocodeService


reverse_geo = APIRouter(
    prefix="/api/v1/satellite",
    tags=["Reverse Geocode"],
    dependencies=[Depends(StaticBearer)],
)


@reverse_geo.get(
    "/reverse-geocode",
    name="Convert your latlong to address",
)
async def reverse_geocode(  # noqa: ANN201
    request: Request,
    payload: Annotated[QueryParamsCoordinate, Query()],
):
    reverse_geocode_service: ReverseGeocodeService = request.state.reverse_geocode_service
    response = await reverse_geocode_service.reverse_geocode(
        payload=payload,
    )
    return JsonResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        data=response,
        message="Get Address Success",
    )
