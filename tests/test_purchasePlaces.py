import server
from flask import get_flashed_messages


def test_purchase_places_success(client):
    success_msg = "Great-booking complete, with 2 places booked"
    test_data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    }

    response = client.post('/purchasePlaces', data=test_data,
                           follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("success", success_msg) in flashed_messages

    assert int(server.competitions[0]['numberOfPlaces']) == 23
    assert int(server.clubs[0]['points']) == 11


def test_competition_full_message(client):
    competition = next(
        (c for c in server.competitions if c['name'] == 'Spring Festival'),
        None)
    competition['numberOfPlaces'] = '0'
    error_msg = "This competition is full."
    test_data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '1'
    }

    response = client.post('/purchasePlaces', data=test_data,
                           follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_points_deduction_after_purchase(client):
    initial_points = int(server.clubs[0]['points'])
    test_data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    }
    response = client.post('/purchasePlaces', data=test_data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert int(server.clubs[0]['points']) == initial_points - 2


def test_purchase_more_than_12_places(client):
    error_msg = "You cannot reserve more than 12 places per competition"
    test_data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    }
    response = client.post('/purchasePlaces', data=test_data,
                           follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_prevent_overbooking(client):
    error_msg = "Not enough places available"
    test_data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '50'
    }
    response = client.post('/purchasePlaces', data=test_data,
                           follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        flashed_messages = get_flashed_messages(with_categories=True)
        assert ("error", error_msg) in flashed_messages


def test_points_not_deducted_if_more_than_12_places(client):
    initial_points = int(server.clubs[0]['points'])
    test_data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    }
    response = client.post('/purchasePlaces', data=test_data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert int(server.clubs[0]['points']) == initial_points
