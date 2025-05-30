from contextlib import ExitStack
from dataclasses import asdict, dataclass
import pytest
from unittest.mock import patch
import requests
from pytest import Mark, MarkDecorator, FixtureRequest
from typing import Any, ClassVar, Collection, NamedTuple


class MockFunction(NamedTuple):
    '''Used for the `patch` function.'''
    target: str
    return_value: Any = None
    side_effect: Exception | None = None


@dataclass(kw_only=True)
class TestCase:
    '''Dataclass that contains information for the `pytest.param` function.'''
    marks: MarkDecorator | Collection[MarkDecorator | Mark] = ()
    label: str | None = None

    _excluded_fields: ClassVar[set[str]] = {'marks', 'label'}

    @property
    def _values(self):
        '''Values of the parameter set for the`pytest.param` function, in order.'''
        # Order is ensured because dictionaries maintain insertion order by default
        return tuple(v for k, v in asdict(self).items() if k not in self._excluded_fields)

    def to_parameter_set(self):
        '''Create a `ParameterSet` object for parameterizing.'''
        return pytest.param(*self._values, marks=self.marks, id=self.label)


def _create_parameter_set_list(tests: list[TestCase]):
    '''Create a `ParameterSet` list using the `TestCase` object's `to_parameter_set` method.'''
    return [test.to_parameter_set() for test in tests]


def setup_pytest_generate_tests(metafunc: pytest.Metafunc, config: dict[str, tuple | list[TestCase] | list[str]]):
    '''Setup for the hook function for pytest to dynamically parameterize tests.'''
    if config:
        argnames = config["argnames"]
        argvalues = _create_parameter_set_list(config['tests'])
        indirect = config.get('indirect', False)

        # Parameterize the test function and ENSURE parameters are matched to the test function's signature
        metafunc.parametrize(argnames, argvalues, indirect)


@pytest.fixture
def mock_fns(request: FixtureRequest):
    '''Fixture that patches and mocks one or more functions.'''

    # Normalize to an iterable if only one MockFunction is passed
    param = request.param
    if isinstance(param, MockFunction):
        param = [param]

    # Dynamically manage patching
    mocks = []
    with ExitStack() as stack:
        for target, return_value, side_effect in param:
            mock = stack.enter_context(patch(target, side_effect=side_effect))
            # Optionally set return value because fastapi can fail
            if return_value is not None:
                mock.return_value = return_value
            mocks.append(mock)
        yield mocks


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
