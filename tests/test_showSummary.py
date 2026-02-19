def test_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'test@test.com'})
    assert response.status_code == 200
    assert b'Cet email est inconnu' in response.data


def test_invalid_email_format(client):
    response = client.post('/showSummary', data={'email': 'test@'})
    assert response.status_code == 200
    assert b'Cet email ne correspond pas au format attendu' in response.data


def test_valid_email(client):
    response = client.post('/showSummary', data={'email': 'club@test.com'})
    assert response.status_code == 200
    assert b'Welcome' in response.data
