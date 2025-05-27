from fastapi.testclient import TestClient

_ROUTE = 'news'


def test_get_space_news(mock_fn, params: dict | None, expected_status_code: int, test_client: TestClient):
    url = f'{_ROUTE}'
    response = test_client.get(url, params=params)
    assert response.status_code == expected_status_code


def test_get_space_industry_news(mock_fn, params: dict | None, expected_status_code: int, test_client: TestClient):
    url = f'{_ROUTE}/industry'
    response = test_client.get(url, params=params)
    assert response.status_code == expected_status_code


def test_get_space_science_news(mock_fn, params: dict | None, expected_status_code: int, test_client: TestClient):
    url = f'{_ROUTE}/science'
    response = test_client.get(url, params=params)
    assert response.status_code == expected_status_code
