import pytest
from server import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
    })
    return flask_app
