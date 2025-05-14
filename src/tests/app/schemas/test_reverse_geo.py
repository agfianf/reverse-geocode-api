import pytest

from pydantic import ValidationError

from app.schemas.reverse_geo import AddressLocation, QueryParamsCoordinate


@pytest.fixture
def valid_query_params():
    return {"lat": -6.2, "lng": 106.8}


def test_query_params_coordinate_valid(valid_query_params):
    params = QueryParamsCoordinate(**valid_query_params)
    assert params.lat == -6.2
    assert params.lng == 106.8


def test_query_params_coordinate_invalid():
    with pytest.raises(ValidationError):
        QueryParamsCoordinate(lat=100.0, lng=200.0)  # Invalid lat/lng


@pytest.fixture
def address_location_data():
    return {
        "sub_district": "Kebayoran Baru",
        "district": "Jakarta Selatan",
        "regency_city": "Jakarta",
        "province": "DKI Jakarta",
        "country": "Indonesia",
    }


def test_address_location_valid(address_location_data):
    address = AddressLocation(**address_location_data)
    assert address.sub_district == "Kebayoran Baru"
    assert address.district == "Jakarta Selatan"
    assert address.regency_city == "Jakarta"
    assert address.province == "DKI Jakarta"
    assert address.country == "Indonesia"


def test_address_location_partial():
    address = AddressLocation(sub_district="Kebayoran Baru")
    assert address.sub_district == "Kebayoran Baru"
    assert address.district is None
    assert address.regency_city is None
    assert address.province is None
    assert address.country is None
