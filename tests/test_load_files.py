import json
from unittest.mock import mock_open, patch
from server import load_clubs, load_competitions

club_data = {
    "clubs": [
        {
            "name": "Club Test 1",
            "email": "john.doen@clubtest.com",
            "points": "13"
        }
    ]
}
competition_data = {
    "competitions": [
        {
            "name": "Competition Test 1",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
}


def test_load_clubs_success():
    m = mock_open(read_data=json.dumps(club_data))
    with patch('builtins.open', m):
        result = load_clubs()

    assert result == club_data["clubs"]


def test_load_clubs_file_not_found():
    with patch(
            'builtins.open',
            side_effect=FileNotFoundError("Fichier introuvable")):
        result = load_clubs()
        assert result == {"error": "Le fichier clubs.json est introuvable."}


def test_load_clubs_invalid_json():
    invalid_json_content = "something that's not a json file"
    with patch('builtins.open', mock_open(read_data=invalid_json_content)):
        result = load_clubs()
        assert result == {"error": "Le fichier clubs.json n'est pas un JSON "
                                   "valide."}


def test_load_clubs_missing_key():
    json_content = '{"Clubs tests": ["Club A", "Club B"]}'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = load_clubs()
        assert result == {
            "error": "Le fichier clubs.json ne contient pas de clé 'clubs'."
        }


def test_load_competitions_success():
    m = mock_open(read_data=json.dumps(competition_data))
    with patch('builtins.open', m):
        result = load_competitions()

    assert result == competition_data["competitions"]


def test_load_competitions_file_not_found():
    with patch(
            'builtins.open',
            side_effect=FileNotFoundError("Fichier introuvable")):
        result = load_competitions()
        assert result == {
            "error": "Le fichier competitions.json est introuvable."}


def test_load_competitions_invalid_json():
    invalid_json_content = "something that's not a json file"
    with patch('builtins.open', mock_open(read_data=invalid_json_content)):
        result = load_competitions()
        assert result == {"error": "Le fichier competitions.json n'est pas un "
                                   "JSON valide."}


def test_load_competitions_missing_key():
    json_content = '{"Competitions tests": ["Competition A", "Competition B"]}'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = load_competitions()
        assert result == {
            "error": "Le fichier competitions.json ne contient pas de clé "
                     "'competitions'."
        }
