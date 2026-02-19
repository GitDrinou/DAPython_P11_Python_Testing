from flask import get_flashed_messages


def test_booking_success(client):
    response = client.get('/book/CompetitionTest/ClubTest')
    assert response.status_code == 200
    assert b'Book Places' in response.data


def test_club_not_found(client):
    response = client.get('/book/CompetitionTest/UnknownClubTest')
    error_msg = "Le club 'UnknownClubTest' n'a pas été trouvé."
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_competition_not_found(client):
    response = client.get('/book/UnknownCompetitionTest/ClubTest')
    error_msg = "La compétition 'UnknownCompetitionTest' n'a pas été trouvée."
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages
