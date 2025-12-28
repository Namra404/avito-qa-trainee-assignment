import uuid
import pytest

from test_task_2_1.utils.endpoints import Endpoints
from test_task_2_1.utils.errors_asserts import assert_error_by_status

ENDPOINT = Endpoints.V2_DELETE_ITEM


@pytest.mark.positive
def test_tc058_v2_delete_item_success(api, created_item_id):
    """TC-058: Удаление существующего объявления по его id"""
    expected_status = 200
    r = api.delete(ENDPOINT.format(created_item_id))
    assert r.status_code == expected_status


@pytest.mark.negative
def test_tc059_v2_delete_invalid_id(api):
    """TC-059: Негативный тест на удаление существующего объявления по невалидному id"""
    expected_status = 400
    r = api.delete(ENDPOINT.format("invalidId"))
    assert r.status_code == expected_status
    assert_error_by_status(r.status_code, r.json())


@pytest.mark.negative
@pytest.mark.xfail(reason="Known bug: HTTP 404 but body.status='500' (inconsistent error contract)")
def test_tc060_v2_delete_not_found(api):
    """Негативный тест на удаление существующего объявления по валидному, но не существующему id"""
    expected_status = 404
    r = api.delete(ENDPOINT.format(str(uuid.uuid4())))
    assert r.status_code == expected_status
    body = r.json()
    assert_error_by_status(r.status_code, body)