from flask import get_flashed_messages


def login_as(client, club_name="Simply Lift"):
    with client.session_transaction() as sess:
        sess["club"] = club_name


def test_booking_success(client):
    login_as(client)
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'<form action="/purchasePlaces"' in response.data
    assert b'<button type="submit">Book</button>' in response.data


def test_club_not_found(client):
    login_as(client)
    response = client.get('/book/Spring Festival/UnknownClubTest')
    error_msg = "The club 'UnknownClubTest' was not found."
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_competition_not_found(client):
    login_as(client)
    response = client.get('/book/UnknownCompetitionTest/Simply Lift')
    error_msg = "The competition 'UnknownCompetitionTest' was not found."
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages
