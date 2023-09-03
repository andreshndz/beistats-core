import pytest
from fastapi.testclient import TestClient

from beistats_core.app import app


@pytest.fixture
def client():
    return TestClient(app)
