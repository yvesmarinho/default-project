from __future__ import annotations

import pytest

from src.app import create_app


@pytest.fixture
def app():
    """Flask app em modo testing."""
    application = create_app("testing")
    yield application


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()
