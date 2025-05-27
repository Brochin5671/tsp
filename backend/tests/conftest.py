import pytest
from src.models import Article
from src.helpers import datetime_UTC_Week
from unittest.mock import patch
import requests


@pytest.fixture
def mock_get_exception():
    with patch('requests.get') as mock:
        mock.return_value.raise_for_status.side_effect = requests.HTTPError(
            "Internal Server Error")
        yield


@pytest.fixture(scope='module')
def mock_articles() -> list[Article]:
    # Mocks extracted article data from sources
    articles = []
    for i in range(10):
        article = Article(title=f'title_{i}', content=f'content_{i}', author=f'author_{i}', image=f'image_{i}',
                          url=f'https://example{i}.com/', timestamp=i, category='Test')
        articles.append(article)
    return articles


@pytest.fixture(scope='module')
def mock_articles_result(mock_articles) -> list[Article]:
    # Mocks aggregated article data
    return sorted(mock_articles,
                  key=lambda x: x.timestamp,
                  reverse=True)[:5]


@pytest.fixture(scope='module')
def mock_datetime():
    return datetime_UTC_Week()


@pytest.fixture
def mock_request_get_json_cached():
    with patch('src.helpers.request_get_json_cached') as mock:
        mock.return_value = None
        yield
