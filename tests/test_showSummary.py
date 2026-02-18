def test_unknown_email(client):
    response= client.post('/showSummary', data={'email': 'test@test.com'})
    assert response.status_code == 200
    assert b'Cet email est inconnu' in response.data
