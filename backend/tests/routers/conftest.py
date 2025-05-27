from main import app

from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope='session')
def test_client():
    client = TestClient(app)
    yield client
