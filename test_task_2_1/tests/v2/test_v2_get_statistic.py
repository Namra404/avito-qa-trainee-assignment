import pytest
import uuid

from test_task_2_1.utils.endpoints import Endpoints
from test_task_2_1.utils.errors_asserts import assert_error_by_status

ENDPOINT = Endpoints.V2_GET_STATISTIC


@pytest.mark.positive
def test_tc054_v2_get_statistic_success(api, created_item_id):
    """TC-054: v2 статистика по существующему id -> 200."""
    expected_status = 200
    r = api.get(ENDPOINT.format(created_item_id))
    assert r.status_code == expected_status

    data = r.json()
    assert isinstance(data, list)



@pytest.mark.negative
@pytest.mark.parametrize(
    "item_id, expected_status",
    [
        (str(uuid.uuid4()), 404),  # TC-055

        pytest.param(
            "invalidId", 404,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 404 but body.status == '400' (inconsistent error contract)",
                strict=False
            ),
            id="TC-056"
        ),

        pytest.param(
            "x" * 700, 404,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 404 but body.status == '400' (inconsistent error contract)",
                strict=False
            ),
            id="TC-057"
        ),
    ],
    ids=["TC-055", "TC-056", "TC-057"],
)
def test_v2_get_statistic_negative(api, item_id, expected_status):
    """Негативные сценарии v2 статистики."""
    r = api.get(ENDPOINT.format(item_id))
    assert r.status_code == expected_status
    assert_error_by_status(r.status_code, r.json())