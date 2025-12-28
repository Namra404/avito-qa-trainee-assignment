import uuid
import pytest

from test_task_2_1.utils.endpoints import Endpoints
from test_task_2_1.utils.errors_asserts import assert_error_by_status

ENDPOINT = Endpoints.V1_GET_STATISTIC


def assert_stat_item_shape(item: dict):
    """Проверка на наличие всех полей в ответе GET /api/1/statistic/{}"""
    assert isinstance(item, dict)
    for k in ["likes", "viewCount", "contacts"]:
        assert k in item


@pytest.mark.positive
def test_tc042_get_statistic_success(api, created_item_id):
    """TC-042: статистика по существующему возвращается массив объектов."""
    expected_status = 200
    r = api.get(ENDPOINT.format(created_item_id))
    assert r.status_code == expected_status

    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    for item in data:
        assert_stat_item_shape(item)


@pytest.mark.negative
@pytest.mark.parametrize(
    "item_id, expected_status",
    [
        ("invalidId", 400),           # TC-043
        (str(uuid.uuid4()), 404),     # TC-044
        (":id", 400),                 # TC-045
        ("x" * 700, 400),             # TC-046
    ],
    ids=["TC-043", "TC-044", "TC-045", "TC-046"],
)
def test_get_statistic_negative(api, item_id, expected_status):
    """Негативное получение статистики объявления по невалидному id."""
    r = api.get(ENDPOINT.format(item_id))
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())
