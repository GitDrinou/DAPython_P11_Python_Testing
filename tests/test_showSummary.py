from flask import get_flashed_messages


def test_unknown_email(client):
    error_msg = ("No clubs were found with this email address. Please try "
                 "again.")
    response = client.post(
        '/showSummary',
        data={'email': 'test@test.com'},
        follow_redirects=True
    )
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_invalid_email_format(client):
    error_msg = "Invalid email format. Please try again."
    response = client.post(
        '/showSummary',
        data={'email': 'test@'},
        follow_redirects=True
    )
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_valid_email(client):
    response = client.post(
        '/showSummary',
        data={'email': 'club@test.com'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_logout_success(client):
    client.post('/', data={'email': 'club@test.com'}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("info", "You have been logged out.") in flashed_messages
