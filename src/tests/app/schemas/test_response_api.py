import pytest

from pydantic import ValidationError

from app.schemas.response_api import JsonResponse, MetaResponse


@pytest.fixture
def meta_response_data():
    return {
        "current_page": 1,
        "page_size": 10,
        "prev_page": False,
        "next_page": True,
        "total_pages": 5,
        "total_items": 50,
    }


def test_meta_response_valid(meta_response_data):
    meta = MetaResponse(**meta_response_data)
    assert meta.current_page == 1
    assert meta.page_size == 10
    assert meta.prev_page is False
    assert meta.next_page is True
    assert meta.total_pages == 5
    assert meta.total_items == 50


def test_json_response_valid(meta_response_data):
    data = {"foo": "bar"}
    meta = MetaResponse(**meta_response_data)
    response = JsonResponse(
        data=data, message="Success", success=True, meta=meta, status_code=200
    )
    assert response.data == data
    assert response.message == "Success"
    assert response.success is True
    assert response.meta == meta
    assert response.status_code == 200


def test_json_response_missing_status_code(meta_response_data):
    data = {"foo": "bar"}
    meta = MetaResponse(**meta_response_data)
    with pytest.raises(ValidationError):
        JsonResponse(data=data, message="Success", success=True, meta=meta)
