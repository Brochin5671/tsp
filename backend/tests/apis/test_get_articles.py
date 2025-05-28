from src.apis.get_articles import get_SNAPI_articles, get_physorg_articles, get_industry_articles, get_science_articles, get_all_articles
from unittest.mock import patch


limit = 5


def test_get_SNAPI_articles(mock_datetime):
    articles = get_SNAPI_articles(mock_datetime)
    assert articles
    # Test that articles are returned after the earliest datetime
    timestamp = mock_datetime.timestamp()
    assert all(article.timestamp >= timestamp for article in articles)


def test_get_physorg_articles(mock_datetime):
    articles = get_physorg_articles(mock_datetime)
    assert articles
    # Test that articles are returned after the datetime
    timestamp = mock_datetime.timestamp()
    assert all(article.timestamp >= timestamp for article in articles)


@patch('src.apis.get_articles.get_SNAPI_articles')
def test_get_industry_articles(mock_SNAPI, mock_articles, mock_datetime, mock_articles_result):
    mock_SNAPI.return_value = mock_articles
    articles = get_industry_articles(mock_datetime, limit)
    assert articles == mock_articles_result


@patch('src.apis.get_articles.get_physorg_articles')
def test_get_science_articles(mock_physorg, mock_articles, mock_datetime, mock_articles_result):
    mock_physorg.return_value = mock_articles
    articles = get_science_articles(mock_datetime, limit)
    assert articles == mock_articles_result


@patch('src.apis.get_articles.get_industry_articles')
@patch('src.apis.get_articles.get_science_articles')
def test_get_all_articles(mock_science, mock_industry, mock_articles, mock_datetime, mock_articles_result):
    # Ensure results are combined (they will be for this case)
    mock_industry.return_value = mock_articles[:3]
    mock_science.return_value = mock_articles[3:]
    articles = get_all_articles(mock_datetime, limit)
    assert articles == mock_articles_result
