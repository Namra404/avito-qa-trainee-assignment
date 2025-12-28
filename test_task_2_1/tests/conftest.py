import pytest
from test_task_2_1.utils.client import ApiClient

def _make_valid_body():
    """Базовый валидный body для POST /api/1/item"""
    return {
        "sellerID": 210800,
        "name": "Phone",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }


def build_body(overrides: dict):
    """
    Берем валидный body и поверх накладываем изменения.
    Для удаления поля - в overrides нужно передать "__REMOVE__".
    """
    body = _make_valid_body()

    for key, value in overrides.items():
        if key == "statistics" and isinstance(value, dict):
            body["statistics"].update(value)
        else:
            body[key] = value

    for key, value in list(body.items()):
        if value == "__REMOVE__":
            del body[key]

    if "statistics" in body and isinstance(body["statistics"], dict):
        for k, v in list(body["statistics"].items()):
            if v == "__REMOVE__":
                del body["statistics"][k]

    return body


def assert_item_has_required_fields(item: dict):
    """Минимальная проверка структуры объявления в ответе для GET запросов"""
    assert isinstance(item, dict)

    required_keys = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
    for k in required_keys:
        assert k in item

    stats = item["statistics"]
    assert isinstance(stats, dict)

    required_stats = ["likes", "viewCount", "contacts"]
    for k in required_stats:
        assert k in stats


# fixtures

@pytest.fixture(scope="session")
def api():
    """Один клиент на весь прогон."""
    return ApiClient()


@pytest.fixture()
def valid_post_body():
    """Валидный body (новый dict на каждый тест)."""
    return _make_valid_body()


@pytest.fixture()
def created_item_id(api, valid_post_body):
    """
    Создаёт объявление и возвращает id.
    PS. По контракту должен быть data["id"], но если сервис багует и возвращает только status,
    берём UUID как последний кусок строки.
    """
    r = api.post("/api/1/item", json_body=valid_post_body)
    assert r.status_code == 200, f"Can't create item: {r.status_code} {r.text}"

    data = r.json()

    if isinstance(data, dict) and "id" in data:
        return data["id"]

    if isinstance(data, dict) and "status" in data and isinstance(data["status"], str):
        return data["status"].split()[-1]

    pytest.fail(f"Unexpected create item response: {data}")


@pytest.fixture()
def existing_seller_id(valid_post_body, created_item_id):
    """
    Возвращает валидный sellerID из специально созданного объявления.
    """
    return valid_post_body["sellerID"]
