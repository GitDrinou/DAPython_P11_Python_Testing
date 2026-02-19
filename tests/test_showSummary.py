from flask import get_flashed_messages


def test_unknown_email(client):
    error_msg = "Aucun club trouvé avec cet email. Veuillez réessayer."
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
    error_msg = "Format d'email invalide. Veuillez réessayer."
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
