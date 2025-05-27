from dataclasses import dataclass
from typing import Any
from src.models import MarsPhotoAPIRoverType
from main import app
from tests.conftest import PytestParam
from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from tests.conftest import create_parameter_set_list
from fastapi import status


@dataclass(kw_only=True)
class PytestParamRouter(PytestParam):
    '''`PytestParam` with additional attributes for testing using FastAPI's `TestClient`.'''
    mock_fn: tuple[str, Any, Exception | None]
    params: dict | None = None
    expected_status_code: int

    def to_parameter_set(self):
        '''Create a `ParameterSet` object for parameterizing.'''
        return pytest.param(self.mock_fn, self.params, self.expected_status_code, id=self.label)


# Test cases for each test function
_GET_SPACE_NEWS_TESTS = [
    PytestParamRouter(label='Default arguments', mock_fn=('space_news', None, None),
                      expected_status_code=status.HTTP_200_OK),
    PytestParamRouter(label='Invalid earliestDatetime', mock_fn=('space_news', None, None), params={'earliestDatetime': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid limit', mock_fn=('space_news', None, None), params={'limit': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid limit: limit >= 0 constraint', mock_fn=('space_news', None, None), params={'limit': -1},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Failure', mock_fn=('space_news', None, Exception()),
                      expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
]
_GET_SPACE_INDUSTRY_NEWS_TESTS = [
    PytestParamRouter(label='Default arguments', mock_fn=('space_industry_news', None, None),
                      expected_status_code=status.HTTP_200_OK),
    PytestParamRouter(label='Invalid earliestDatetime', mock_fn=('space_industry_news', None, None), params={'earliestDatetime': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid limit', mock_fn=('space_industry_news', None, None), params={'limit': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid limit: limit >= 0 constraint', mock_fn=('space_industry_news', None, None), params={'limit': -1},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Failure', mock_fn=('space_industry_news', None, Exception()),
                      expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
]
_GET_SPACE_SCIENCE_NEWS_TESTS = [
    PytestParamRouter(label='Default arguments', mock_fn=('space_science_news', None, None),
                      expected_status_code=status.HTTP_200_OK),
    PytestParamRouter(label='Invalid earliestDatetime', mock_fn=('space_science_news', None, None), params={'earliestDatetime': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid limit', mock_fn=('space_science_news', None, None), params={'limit': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid limit: limit >= 0 constraint', mock_fn=('space_science_news', None, None), params={'limit': -1},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Failure', mock_fn=('space_science_news', None, Exception()),
                      expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
]
_GET_EPIC_API_TESTS = [
    PytestParamRouter(label='Default arguments', mock_fn=('EPIC_API', None, None),
                      expected_status_code=status.HTTP_200_OK),
    PytestParamRouter(label='Invalid collection', mock_fn=('EPIC_API', None, None), params={'collection': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid series', mock_fn=('EPIC_API', None, None), params={'series': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid image_type', mock_fn=('EPIC_API', None, None), params={'image_type': 'tiff'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid date', mock_fn=('EPIC_API', None, None), params={'date': '2019 12 1'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Failure', mock_fn=('EPIC_API', None, Exception()),
                      expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
]
_GET_MARS_PHOTO_API_TESTS = [
    PytestParamRouter(label='Default arguments', mock_fn=('MP_API', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY},
                      expected_status_code=status.HTTP_200_OK),
    PytestParamRouter(label='Invalid rover', mock_fn=('MP_API', None, None), params={'rovers': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid camera', mock_fn=('MP_API', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'cameras': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid earth_date', mock_fn=('MP_API', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY,
                                                                                          'earth_date': '2019 12 1'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid sol', mock_fn=('MP_API', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'sol': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid sol: sol >= 0 constraint', mock_fn=('MP_API', None, None), params={
                      'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'sol': -1}, expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Failure', mock_fn=('MP_API', None, Exception()), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY},
                      expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
]
_GET_MARS_PHOTO_API_METADATA_TESTS = [
    PytestParamRouter(label='Default arguments', mock_fn=('MP_API_meta', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY},
                      expected_status_code=status.HTTP_200_OK),
    PytestParamRouter(label='Invalid rover', mock_fn=('MP_API_meta', None, None), params={'rovers': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid manifest', mock_fn=('MP_API_meta', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'manifest': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid earth_date', mock_fn=('MP_API_meta', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY,
                                                                                               'earth_date': '2019 12 1'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid sol', mock_fn=('MP_API_meta', None, None), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'sol': 'invalid'},
                      expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Invalid sol: sol >= 0 constraint', mock_fn=('MP_API_meta', None, None), params={
                      'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'sol': -1}, expected_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    PytestParamRouter(label='Failure', mock_fn=('MP_API_meta', None, Exception()), params={'rovers': MarsPhotoAPIRoverType.CURIOSITY},
                      expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
]

# Configurations for each test function
_TEST_CONFIGS = {
    'test_get_space_news': {
        'tests': _GET_SPACE_NEWS_TESTS
    },
    'test_get_space_industry_news': {
        'tests': _GET_SPACE_INDUSTRY_NEWS_TESTS
    },
    'test_get_space_science_news': {
        'tests': _GET_SPACE_SCIENCE_NEWS_TESTS
    },
    'test_get_EPIC_API': {
        'tests': _GET_EPIC_API_TESTS,
    },
    'test_get_mars_photo_API': {
        'tests': _GET_MARS_PHOTO_API_TESTS,
    },
    'test_get_mars_photo_API_metadata': {
        'tests': _GET_MARS_PHOTO_API_METADATA_TESTS,
    },
}

# Using a label, maps to the path of each target function for mocking
_FN_PATHS = {
    'space_news': 'src.routers.news.get_all_articles',
    'space_industry_news': 'src.routers.news.get_industry_articles',
    'space_science_news': 'src.routers.news.get_science_articles',
    'EPIC_API': 'src.routers.imagery.get_EPIC_API_images',
    'MP_API': 'src.routers.imagery.get_MP_API_images',
    'MP_API_meta': 'src.routers.imagery.get_MP_API_metadata'
}


@pytest.fixture(scope='package')
def test_client():
    '''Fixture for `TestClient`.'''
    client = TestClient(app)
    yield client


@pytest.fixture
def mock_fn(request: pytest.FixtureRequest):
    '''Fixture that mocks a given function.'''
    label, return_value, side_effect = request.param
    # Get the target function to patch
    target = _FN_PATHS[label]
    with patch(target, side_effect=side_effect) as mock:
        # Optionally set return value because fastapi can fail
        if return_value is not None:
            mock.return_value = return_value
        yield mock


def pytest_generate_tests(metafunc: pytest.Metafunc):
    '''The hook function for pytest to dynamically parameterize `routers` tests.'''
    # Use the test function's name as a key to get the configuration for that test function
    config = _TEST_CONFIGS.get(metafunc.function.__name__)
    if config:

        parameter_set_list = create_parameter_set_list(config["tests"])

        # Parameterize the test function and ENSURE parameters are matched to the test function's signature
        # TODO: maybe this could be simplified to use configuration?
        metafunc.parametrize(
            ("mock_fn", "params", "expected_status_code"),
            parameter_set_list,
            indirect=["mock_fn"]
        )
