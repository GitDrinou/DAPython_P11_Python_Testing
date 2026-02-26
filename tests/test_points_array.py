import server


def test_displaying_club_points(client):
    response = client.get("/points")
    assert response.status_code == 200
    assert b"<table" in response.data
    for club in server.clubs:
        assert club["name"].encode() in response.data
        assert str(club["points"]).encode() in response.data
