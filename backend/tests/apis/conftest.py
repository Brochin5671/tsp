from dataclasses import dataclass
import pytest
from src.models import Article
from src.helpers import datetime_UTC_Week
from unittest.mock import patch


@dataclass(kw_only=True)
class PytestParamApis:
    '''Dataclass that contains information for the `pytest.param` function.'''
    label: str | None = None
    # TODO: add marks

    def to_parameter_set(self):
        '''Create a `ParameterSet` object for parameterizing.'''
        return pytest.param(id=self.label)


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
