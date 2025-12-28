import pytest
from test_task_2_1.tests.conftest import build_body
from test_task_2_1.utils.endpoints import Endpoints
from test_task_2_1.utils.errors_asserts import assert_error_by_status

ENDPOINT = Endpoints.V1_CREATE_ITEM


@pytest.mark.positive
@pytest.mark.xfail(reason="Known bug: POST /api/1/item returns only status instead of full created object")
def test_tc001_create_item_success(api, valid_post_body):
    """TC-001: Создание объявления, по контракту должен вернуться объект объявления."""
    r = api.post(ENDPOINT, json_body=valid_post_body)
    assert r.status_code == 200

    data = r.json()
    required = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
    for k in required:
        assert k in data


@pytest.mark.negative
@pytest.mark.xfail(
    reason="Known bug: for HTTP 400 body.status is not '400' (returns text like 'не передан объект - объявление')")
def test_tc002_create_item_missing_body(api):
    """TC-002: Создание без объявления без body."""
    expected_status = 400
    r = api.post(ENDPOINT, json_body=None)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())


@pytest.mark.negative
@pytest.mark.parametrize(
    "overrides, expected_status, expected_message",
    [
        ({"statistics": {"likes": "__REMOVE__"}}, 400, "поле likes обязательно"),
        ({"statistics": {"viewCount": "__REMOVE__"}}, 400, "поле viewCount обязательно"),
        ({"statistics": {"contacts": "__REMOVE__"}}, 400, "поле contacts обязательно"),
    ],
    ids=["TC-003", "TC-004", "TC-005"],
)
def test_tc003_005_missing_required_stats_fields(api, overrides, expected_status, expected_message):
    """TC-003-005: Создание объявления с отсутствующими обязательными поли в statistics."""
    body = build_body(overrides)
    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    data = r.json()
    assert_error_by_status(expected_status, data)


@pytest.mark.negative
@pytest.mark.parametrize(
    "overrides, expected_status",
    [
        ({}, 400),  # TC-006 empty json
        ({"statistics": "__REMOVE__"}, 400),  # TC-007
        ({"statistics": None}, 400),  # TC-023

        pytest.param(
            {"statistics": "bad"}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"),
            id="TC-024"
        ),  # TC-024

        pytest.param(
            {"statistics": []}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"),
            id="TC-025"
        ),  # TC-025
    ],
    ids=["TC-006", "TC-007", "TC-023", "TC-024", "TC-025"],
)
def test_post_item_invalid_statistics_type(api, overrides, expected_status):
    """Создание объявления с невалидным statistics."""
    if overrides == {}:
        body = {}  # для TC-006
    else:
        body = build_body(overrides)

    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())


@pytest.mark.negative
@pytest.mark.parametrize(
    "overrides, expected_status",
    [
        ({"sellerID": "__REMOVE__"}, 400),  # TC-008
        ({"sellerID": None}, 400),  # TC-009

        pytest.param(
            {"sellerID": "210800"}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"),
            id="TC-010"
        ),

        ({"sellerID": 0}, 400),  # TC-011
    ],
    ids=["TC-008", "TC-009", "TC-010", "TC-011"],
)
def test_post_item_invalid_seller_id(api, overrides, expected_status):
    """Негативные тесты по созданию объявления с невалидным sellerID."""
    body = build_body(overrides)
    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())


@pytest.mark.negative
@pytest.mark.parametrize(
    "overrides, expected_status",
    [
        ({"name": "__REMOVE__"}, 400),  # TC-013
        ({"name": None}, 400),  # TC-014
        ({"name": ""}, 400),  # TC-015

        pytest.param(
            {"name": 123}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"),
            id="TC-016"
        ),  # TC-016
    ],
    ids=["TC-013", "TC-014", "TC-015", "TC-016"],
)
def test_post_item_invalid_name(api, overrides, expected_status):
    """Негативные тесты по созданию объявления с невалидным name."""
    body = build_body(overrides)
    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())


@pytest.mark.negative
@pytest.mark.parametrize(
    "overrides, expected_status",
    [
        ({"price": "__REMOVE__"}, 400),  # TC-017
        ({"price": None}, 400),  # TC-018

        pytest.param(
            {"price": "1000"}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"),
            id="TC-019"
        ),  # TC-019

        ({"price": 0}, 400),  # TC-021

        pytest.param(
            {"price": 1000.5}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"),
            id="TC-022"
        ),  # TC-022
    ],
    ids=["TC-017", "TC-018", "TC-019", "TC-021", "TC-022"],
)
def test_post_item_invalid_price(api, overrides, expected_status):
    """Негативные тесты по созданию объявления с невалидным price."""
    body = build_body(overrides)
    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())



@pytest.mark.negative
@pytest.mark.parametrize(
    "overrides, expected_status",
    [
        ({"statistics": {"likes": None}}, 400),        # TC-026
        ({"statistics": {"viewCount": None}}, 400),    # TC-027
        ({"statistics": {"contacts": None}}, 400),     # TC-028

        pytest.param(
            {"statistics": {"likes": "1"}}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"
            ),
            id="TC-029"
        ),

        pytest.param(
            {"statistics": {"viewCount": "1"}}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"
            ),
            id="TC-030"
        ),

        pytest.param(
            {"statistics": {"contacts": "1"}}, 400,
            marks=pytest.mark.xfail(
                reason="Known bug: HTTP 400 but body.status is not '400' (returns 'не передано тело объявления')"
            ),
            id="TC-031"
        ),
    ],
    ids=["TC-026", "TC-027", "TC-028", "TC-029", "TC-030", "TC-031"],
)
def test_tc026_031_invalid_stats_fields_values(api, overrides, expected_status):
    """TC-026..TC-031: statistics поля = null или неверный тип -> 400."""
    body = build_body(overrides)
    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())



@pytest.mark.negative
@pytest.mark.xfail(reason="Known bug: negative values are accepted (should be 400)")
@pytest.mark.parametrize(
    "overrides, expected_status",
    [
        ({"sellerID": -1}, 400),  # TC-012
        ({"price": -1000}, 400),  # TC-020
        ({"statistics": {"likes": -1}}, 400),  # TC-032
        ({"statistics": {"viewCount": -1}}, 400),  # TC-033
        ({"statistics": {"contacts": -1}}, 400),  # TC-034
    ],
    ids=["TC-012", "TC-020", "TC-032", "TC-033", "TC-034"],
)
def test_post_item_negative_values_should_be_400(api, overrides, expected_status):
    """Негативные тесты по созданию объяввления с негативными значеними"""
    body = build_body(overrides)
    r = api.post(ENDPOINT, json_body=body)
    assert r.status_code == expected_status
    assert_error_by_status(expected_status, r.json())
