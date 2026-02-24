def test_book_required_login(client):
    response = client.get('/book/Spring Festival/Simply Lift',
                          follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in" in response.data
