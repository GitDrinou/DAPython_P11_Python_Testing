import json
import server


def test_purchase_places_persists_points_to_clubs_json(client, tmp_path):
    clubs_file = tmp_path / "clubs.json"
    clubs_file.write_text(json.dumps({
        "clubs": [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
        ]
    }))

    old_path = server.CLUBS_FILE
    server.CLUBS_FILE = str(clubs_file)

    try:
        test_data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "2"
        }
        response = client.post("/purchasePlaces", data=test_data,
                               follow_redirects=True)
        assert response.status_code == 200

        saved = json.loads(clubs_file.read_text())
        saved_club = next(
            c for c in saved["clubs"] if c["name"] == "Simply Lift"
        )
        assert saved_club["points"] == "11"
    finally:
        server.CLUBS_FILE = old_path


def test_purchase_places_persists_competition_updates_to_competitions_json(
    client, tmp_path
):
    competitions_file = tmp_path / "competitions.json"
    competitions_file.write_text(json.dumps({
        "competitions": [
            {
                "name": "Spring Festival",
                "date": "2025-03-27 10:00:00",
                "numberOfPlaces": "25"},
            {
                "name": "Fall Classic",
                "date": "2025-10-22 13:30:00",
                "numberOfPlaces": "13"
            },
        ]
    }))

    old_path = server.COMPETITIONS_FILE
    server.COMPETITIONS_FILE = str(competitions_file)

    try:
        test_data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "2"
        }
        response = client.post("/purchasePlaces", data=test_data,
                               follow_redirects=True)
        assert response.status_code == 200

        saved = json.loads(competitions_file.read_text())
        save_competitions = next(
            c for c in saved["competitions"] if c["name"] == "Spring Festival"
        )

        assert int(save_competitions["numberOfPlaces"]) == 23
        assert "bookings_by_club" in save_competitions
        assert int(save_competitions["bookings_by_club"]["Simply Lift"]) == 2
    finally:
        server.COMPETITIONS_FILE = old_path
