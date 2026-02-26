def test_book_requires_login(client):

    response = client.get(
        "/book/Spring Festival/Simply Lift",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You must be logged in to access this page." in response.data


def test_login_sets_session(client):

    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Welcome" in response.data
