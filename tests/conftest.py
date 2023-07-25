import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient


@pytest.fixture(scope='session', autouse=True)
def load_env():
    env_file = find_dotenv('.env.test', raise_error_if_not_found=True)
    load_dotenv(env_file, override=True)


@pytest.fixture
def test_client():
    from app.main import app
    yield TestClient(app)
