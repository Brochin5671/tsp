from unittest.mock import patch

from fastapi.encoders import jsonable_encoder

route = 'news'


@patch('src.routers.news.get_all_articles')
def test_get_space_news(mock_get_all_articles, mock_articles_result, client):
    mock_get_all_articles.return_value = mock_articles_result
    response = client.get(f'{route}/')
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_articles_result)


@patch('src.routers.news.get_industry_articles')
def test_get_space_industry_news(mock_get_industry_articles, mock_articles_result, client):
    mock_get_industry_articles.return_value = mock_articles_result
    response = client.get(f'{route}/industry/')
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_articles_result)


@patch('src.routers.news.get_science_articles')
def test_get_space_science_news(mock_get_science_articles, mock_articles_result, client):
    mock_get_science_articles.return_value = mock_articles_result
    response = client.get(f'{route}/science/')
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_articles_result)
