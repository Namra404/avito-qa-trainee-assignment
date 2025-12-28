import uuid
import pytest
from test_task_2_1.tests.conftest import assert_item_has_required_fields
from test_task_2_1.utils.endpoints import Endpoints
from test_task_2_1.utils.errors_asserts import assert_error_by_status

ENDPOINT = Endpoints.V1_GET_ITEM_BY_ID

@pytest.mark.positive
def test_tc035_get_item_by_id_success(api, created_item_id):
    """TC-035: GET по существующему id, возвращается массив объектов"""
    expected_status = 200
    r = api.get(ENDPOINT.format(created_item_id))
    assert r.status_code == expected_status

    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    for item in data:
        assert_item_has_required_fields(item)

    ids = [item.get("id") for item in data]
    assert created_item_id in ids


@pytest.mark.negative
@pytest.mark.parametrize(
    "item_id, expected_status",
    [
        ("uncorrectId", 400),                 # TC-036
        (str(uuid.uuid4()), 404),             # TC-037
        (":id", 400),                         # TC-038
        ("%0A!@", 400),                       # TC-039
        ("' OR '1'='1' --", 400),              # TC-040
        ("x" * 700, 400),                     # TC-041
    ],
    ids=["TC-036", "TC-037", "TC-038", "TC-039", "TC-040", "TC-041"],
)
def test_get_item_by_id_negative(api, item_id, expected_status):
    """Негативное получение объявлений с невалидными id."""
    r = api.get(ENDPOINT.format(item_id))
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())
