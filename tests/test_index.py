def test_index_page_renders(client):
    response = client.get("/")

    assert response.status_code == 200

    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b'<form action="showSummary" method="post">' in response.data
    assert b"Please enter your secretary email to continue:" in response.data
