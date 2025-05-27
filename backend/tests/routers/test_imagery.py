from fastapi.testclient import TestClient

_ROUTE = 'imagery'


def test_get_EPIC_API(mock_fn, params: dict | None, expected_status_code: int, test_client: TestClient):
    url = f'{_ROUTE}/epic'
    response = test_client.get(url, params=params)
    assert response.status_code == expected_status_code


def test_get_mars_photo_API(mock_fn, params: dict | None, expected_status_code: int, test_client: TestClient):
    url = f'{_ROUTE}/mars-photo'
    response = test_client.get(url, params=params)
    assert response.status_code == expected_status_code


def test_get_mars_photo_API_metadata(mock_fn, params: dict | None, expected_status_code: int, test_client: TestClient):
    url = f'{_ROUTE}/mars-photo/meta'
    response = test_client.get(url, params=params)
    assert response.status_code == expected_status_code
