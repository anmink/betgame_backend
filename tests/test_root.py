def test_root_says_api_is_running(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API läuft"}
