import pytest
from test_task_2_1.tests.conftest import assert_item_has_required_fields
from test_task_2_1.utils.endpoints import Endpoints
from test_task_2_1.utils.errors_asserts import assert_error_by_status

ENDPOINT = Endpoints.V1_GET_SELLER_ITEMS

@pytest.mark.positive
def test_tc047_get_seller_items_success(api, existing_seller_id):
    """TC-047: Получение всех объявления пользователя по валидному sellerID"""
    expected_status = 200
    r = api.get(ENDPOINT.format(existing_seller_id))
    assert r.status_code == expected_status

    data = r.json()
    assert isinstance(data, list)

    for item in data:
        assert_item_has_required_fields(item)


@pytest.mark.negative
def test_tc048_invalid_seller_id(api):
    """TC-048: Негативный тест на получение всех объявления пользователя по невалидному sellerID"""
    expected_status = 400
    r = api.get(ENDPOINT.format("invalidSellerID"))
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())

@pytest.mark.negative
def test_tc049_seller_id_float(api):
    """TC-049: Негативный тест на получение всех объявления пользователя по дробному sellerID"""
    expected_status = 400

    r = api.get(ENDPOINT.format("123.45"))

    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())

@pytest.mark.negative
@pytest.mark.xfail(reason="Known bug: if sellerID contains '#', API returns HTTP 404 but body has code=400")
def test_tc050_seller_id_special_chars(api):
    """TC-050: Негативный тест на получение всех объявления пользователя по sellerID в виде спец.символа #"""
    expected_status = 404
    r = api.get(ENDPOINT.format("#"))
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())


@pytest.mark.negative
@pytest.mark.parametrize(
    "seller_id, expected_status",
    [
        (" ", 400),         # TC-051
        ("x" * 700, 400),   # TC-052
    ],
    ids=["TC-051", "TC-052"],
)
def test_tc051_052_bad_seller_id(api, seller_id, expected_status):
    """TC-051..052: Негативный тест на получение всех объявления пользователя по пробелу/слишком длинноому sellerID """
    r = api.get(ENDPOINT.format(seller_id))
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())


@pytest.mark.negative
@pytest.mark.xfail(reason="Known bug: sellerID=-1 is accepted (should be 400)")
def test_tc053_negative_seller_id(api):
    """TC-053: Негативный тест на получение всех объявления пользователя по отрицательному sellerID"""
    expected_status = 400
    r = api.get(ENDPOINT.format(-1))
    assert r.status_code == expected_status
