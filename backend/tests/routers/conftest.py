from dataclasses import dataclass
from typing import Any, ClassVar, Collection
from src.models import MarsPhotoAPIRoverType
from main import app
from tests.conftest import MockFunction, TestCase, setup_pytest_generate_tests
from fastapi import status
from fastapi.testclient import TestClient
import pytest


@dataclass(kw_only=True)
class RouterTestCase(TestCase):
    '''Dataclass that extends `TestCase` for testing with FastAPI's `TestClient`.'''
    params: dict[str, Any] | None = None
    mock_fns: MockFunction | Collection[MockFunction]
    expected_status_code: int = status.HTTP_200_OK
    is_invalid: bool = False

    _excluded_fields: ClassVar[
        set[str]] = TestCase._excluded_fields | {'is_invalid'}

    def __post_init__(self):

        # Set expected_status_code if testing for invalid parameter
        if self.is_invalid:
            self.expected_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


# Test cases for each test function
_ROUTERS_PATH = 'src.routers.'

_GET_SPACE_NEWS_MOCK_FN_TARGET = f'{_ROUTERS_PATH}news.get_all_articles'
_GET_SPACE_NEWS_MOCK_FN = MockFunction(target=_GET_SPACE_NEWS_MOCK_FN_TARGET)
_GET_SPACE_NEWS_TESTS = [
    RouterTestCase(label='Default arguments',
                   mock_fns=_GET_SPACE_NEWS_MOCK_FN),
    RouterTestCase(label='Invalid earliestDatetime',
                   params={'earliestDatetime': 'invalid'},
                   mock_fns=_GET_SPACE_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid limit',
                   params={'limit': 'invalid'},
                   mock_fns=_GET_SPACE_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid limit: limit >= 0 constraint',
                   params={'limit': -1},
                   mock_fns=_GET_SPACE_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Default failure',
                   mock_fns=MockFunction(
                       target=_GET_SPACE_NEWS_MOCK_FN_TARGET, side_effect=Exception()),
                   expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
]

_GET_SPACE_INDUSTRY_NEWS_MOCK_FN_TARGET = f'{_ROUTERS_PATH}news.get_industry_articles'
_GET_SPACE_INDUSTRY_NEWS_MOCK_FN = MockFunction(
    target=_GET_SPACE_INDUSTRY_NEWS_MOCK_FN_TARGET)
_GET_SPACE_INDUSTRY_NEWS_TESTS = [
    RouterTestCase(label='Default arguments',
                   mock_fns=_GET_SPACE_INDUSTRY_NEWS_MOCK_FN),
    RouterTestCase(label='Invalid earliestDatetime',
                   params={'earliestDatetime': 'invalid'},
                   mock_fns=_GET_SPACE_INDUSTRY_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid limit',
                   params={'limit': 'invalid'},
                   mock_fns=_GET_SPACE_INDUSTRY_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid limit: limit >= 0 constraint',
                   params={'limit': -1},
                   mock_fns=_GET_SPACE_INDUSTRY_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Default failure',
                   mock_fns=MockFunction(
                       target=_GET_SPACE_INDUSTRY_NEWS_MOCK_FN_TARGET, side_effect=Exception()),
                   expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
]

_GET_SPACE_SCIENCE_NEWS_MOCK_FN_TARGET = f'{_ROUTERS_PATH}news.get_science_articles'
_GET_SPACE_SCIENCE_NEWS_MOCK_FN = MockFunction(
    target=_GET_SPACE_SCIENCE_NEWS_MOCK_FN_TARGET)
_GET_SPACE_SCIENCE_NEWS_TESTS = [
    RouterTestCase(label='Default arguments',
                   mock_fns=_GET_SPACE_SCIENCE_NEWS_MOCK_FN),
    RouterTestCase(label='Invalid earliestDatetime',
                   params={'earliestDatetime': 'invalid'},
                   mock_fns=_GET_SPACE_SCIENCE_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid limit',
                   params={'limit': 'invalid'},
                   mock_fns=_GET_SPACE_SCIENCE_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid limit: limit >= 0 constraint',
                   params={'limit': -1},
                   mock_fns=_GET_SPACE_SCIENCE_NEWS_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Default failure',
                   mock_fns=MockFunction(
                       target=_GET_SPACE_SCIENCE_NEWS_MOCK_FN_TARGET, side_effect=Exception()),
                   expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
]

_GET_EPIC_API_MOCK_FN_TARGET = f'{_ROUTERS_PATH}imagery.get_EPIC_API_images'
_GET_EPIC_API_MOCK_FN = MockFunction(target=_GET_EPIC_API_MOCK_FN_TARGET)
_GET_EPIC_API_TESTS = [
    RouterTestCase(label='Default arguments',
                   mock_fns=_GET_EPIC_API_MOCK_FN),
    RouterTestCase(label='Invalid collection',
                   params={'collection': 'invalid'},
                   mock_fns=_GET_EPIC_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid series',
                   params={'series': 'invalid'},
                   mock_fns=_GET_EPIC_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid image_type',
                   params={'image_type': -1},
                   mock_fns=_GET_EPIC_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid date',
                   params={'date': '2019 12 1'},
                   mock_fns=_GET_EPIC_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Default failure',
                   mock_fns=MockFunction(
                       target=_GET_EPIC_API_MOCK_FN_TARGET, side_effect=Exception()),
                   expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
]

_GET_MARS_PHOTO_API_MOCK_FN_TARGET = f'{_ROUTERS_PATH}imagery.get_MP_API_images'
_GET_MARS_PHOTO_API_MOCK_FN = MockFunction(
    target=_GET_MARS_PHOTO_API_MOCK_FN_TARGET)
_GET_MARS_PHOTO_API_TESTS = [
    RouterTestCase(label='Default arguments',
                   params={'rovers': MarsPhotoAPIRoverType.CURIOSITY},
                   mock_fns=_GET_MARS_PHOTO_API_MOCK_FN),
    RouterTestCase(label='Invalid rovers',
                   params={'rovers': 'invalid'},
                   mock_fns=_GET_MARS_PHOTO_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid cameras',
                   params={'cameras': 'invalid'},
                   mock_fns=_GET_MARS_PHOTO_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid earth_date',
                   params={'earth_date': '2019 12 1'},
                   mock_fns=_GET_MARS_PHOTO_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid sol',
                   params={'sol': 'invalid'},
                   mock_fns=_GET_MARS_PHOTO_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid sol: sol >= 0 constraint',
                   params={'sol': -1},
                   mock_fns=_GET_MARS_PHOTO_API_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Default failure',
                   mock_fns=MockFunction(
                       target=_GET_MARS_PHOTO_API_MOCK_FN_TARGET, side_effect=Exception()),
                   expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
]

_GET_MARS_PHOTO_API_METADATA_MOCK_FN_TARGET = f'{_ROUTERS_PATH}imagery.get_MP_API_metadata'
_GET_MARS_PHOTO_API_METADATA_MOCK_FN = MockFunction(
    target=_GET_MARS_PHOTO_API_METADATA_MOCK_FN_TARGET)
_GET_MARS_PHOTO_API_METADATA_TESTS = [
    RouterTestCase(label='Default arguments',
                   mock_fns=_GET_MARS_PHOTO_API_METADATA_MOCK_FN),
    RouterTestCase(label='Invalid rovers',
                   params={'rovers': {'invalid'}},
                   mock_fns=_GET_MARS_PHOTO_API_METADATA_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid manifest',
                   params={'manifest': 'invalid'},
                   mock_fns=_GET_MARS_PHOTO_API_METADATA_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid earth_date',
                   params={'earth_date': '2019 12 1'},
                   mock_fns=_GET_MARS_PHOTO_API_METADATA_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid sol',
                   params={'sol': 'invalid'},
                   mock_fns=_GET_MARS_PHOTO_API_METADATA_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Invalid sol: sol >= 0 constraint',
                   params={'sol': -1},
                   mock_fns=_GET_MARS_PHOTO_API_METADATA_MOCK_FN,
                   is_invalid=True),
    RouterTestCase(label='Default failure',
                   mock_fns=MockFunction(
                       target=_GET_MARS_PHOTO_API_METADATA_MOCK_FN_TARGET, side_effect=Exception()),
                   expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
]

# Configurations for each test function
_ARGNAMES = ('params', 'mock_fns', 'expected_status_code')
_INDIRECT = ['mock_fns']
_TEST_CONFIGS = {
    'test_get_space_news': {
        'argnames': _ARGNAMES,
        'tests': _GET_SPACE_NEWS_TESTS,
        'indirect': _INDIRECT
    },
    'test_get_space_industry_news': {
        'argnames': _ARGNAMES,
        'tests': _GET_SPACE_INDUSTRY_NEWS_TESTS,
        'indirect': _INDIRECT
    },
    'test_get_space_science_news': {
        'argnames': _ARGNAMES,
        'tests': _GET_SPACE_SCIENCE_NEWS_TESTS,
        'indirect': _INDIRECT
    },
    'test_get_EPIC_API': {
        'argnames': _ARGNAMES,
        'tests': _GET_EPIC_API_TESTS,
        'indirect': _INDIRECT
    },
    'test_get_mars_photo_API': {
        'argnames': _ARGNAMES,
        'tests': _GET_MARS_PHOTO_API_TESTS,
        'indirect': _INDIRECT
    },
    'test_get_mars_photo_API_metadata': {
        'argnames': _ARGNAMES,
        'tests': _GET_MARS_PHOTO_API_METADATA_TESTS,
        'indirect': _INDIRECT
    },
}


@pytest.fixture(scope='package')
def test_client():
    '''Fixture for `TestClient`.'''
    client = TestClient(app)
    yield client


def pytest_generate_tests(metafunc: pytest.Metafunc):
    '''The hook function for pytest to dynamically parameterize `routers` tests.'''
    # Use the test function's name as a key to get the configuration for that test function
    config = _TEST_CONFIGS.get(metafunc.function.__name__)
    setup_pytest_generate_tests(metafunc, config)
