from project.app import create_app
import pytest
from config import TestingConfig


@pytest.fixture
def app():
    test_config = TestingConfig()
    _app = create_app(test_config)
    return _app
