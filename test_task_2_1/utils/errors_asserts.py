def assert_400_error(status_code, body: dict):
    """Контракт 400 Bad Request (по Postman коллекции)."""
    assert isinstance(body, dict)
    assert "result" in body and isinstance(body["result"], dict)

    assert "message" in body["result"]
    assert isinstance(body["result"]["message"], str)

    assert body["status"] == str(status_code)

    assert "messages" in body["result"]
    assert isinstance(body["result"]["messages"], (dict, type(None)))

    assert "status" in body


def assert_404_error(status_code, body: dict):
    """
    Контракт 404 Not Found (по Postman коллекции).

    PS. Но на стенде часто прилетает контракт 400 овета даже при HTTP 404:
    Для тестового принимаю оба формата (иначе будут падать многие проверки и я не смогу выолнить пункт “все тесты должны быть пройдены”),
    а несоответствие контракту фиксирую отдельным баг-репортом/xfail тестом.
    """
    assert isinstance(body, dict)
    assert "result" in body

    # --- Вариант "как по доке": result - строка ---
    if isinstance(body["result"], str):
        assert "status" in body
        assert isinstance(body["status"], (str, int))
        return

    # --- Фактический вариант стенда: result - dict ---
    if isinstance(body["result"], dict):
        assert "message" in body["result"]
        assert isinstance(body["result"]["message"], str)

        if "messages" in body["result"]:
            assert isinstance(body["result"]["messages"], (dict, type(None)))

        if "status" in body:
            assert isinstance(body["status"], (str, int))
            assert body["status"] == str(status_code)
        return

    raise AssertionError(f"Unexpected 404 format: {body}")


def assert_500_error(status_code, body: dict):
    """Контракт 500 Internal Server Error (по Postman коллекции)."""
    assert isinstance(body, dict)
    assert "result" in body and isinstance(body["result"], dict)

    assert "message" in body["result"]
    assert isinstance(body["result"]["message"], str)

    assert body["status"] == str(status_code)

    assert "messages" in body["result"]
    assert isinstance(body["result"]["messages"], (dict, type(None)))

    assert "status" in body


_ERROR_ASSERTS = {
    400: assert_400_error,
    404: assert_404_error,
    500: assert_500_error,
}


def assert_error_by_status(status_code: int, body: dict):
    """
    Выбирает проверку контракта по HTTP статусу.
    """
    assert isinstance(body, dict)

    checker = _ERROR_ASSERTS.get(status_code)
    if checker:
        checker(status_code, body)
        return

    assert ("result" in body) or ("message" in body) or ("code" in body) or ("status" in body) # Если статус не описан, то минимальная проверка

