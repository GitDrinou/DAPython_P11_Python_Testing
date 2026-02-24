import pytest
import server


@pytest.fixture
def app():
    server.app.config.update({
        "TESTING": True,
        "SECRET_KEY": "something_special",
        "WTF_CSRF_ENABLED": False,
    })
    return server.app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(autouse=True)
def reset_data():
    server.clubs.clear()
    server.clubs.extend([
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        }
    ])

    server.competitions.clear()
    server.competitions.extend([
        {
            "name": "Spring Festival",
            "date": "2025-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2025-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ])
