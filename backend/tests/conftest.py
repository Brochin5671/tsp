from dataclasses import dataclass
import pytest
from unittest.mock import patch
import requests


@dataclass(kw_only=True)
class PytestParam:
    '''Dataclass that contains information for the `pytest.param` function.'''
    label: str | None = None
    # TODO: add marks

    def to_parameter_set(self):
        '''Create a `ParameterSet` object for parameterizing.'''
        return pytest.param(id=self.label)


def create_parameter_set_list(tests: list[PytestParam]):
    '''Create a `ParameterSet` list using the `PytestParam` object's `to_parameter_set` method.'''
    return [test.to_parameter_set() for test in tests]


@pytest.fixture
def mock_get_exception():
    with patch('requests.get') as mock:
        mock.return_value.raise_for_status.side_effect = requests.HTTPError(
            "Internal Server Error")
        yield


@pytest.fixture
def mock_request_get_json_cached():
    with patch('src.helpers.request_get_json_cached') as mock:
        mock.return_value = None
        yield
