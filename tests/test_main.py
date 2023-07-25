
def test_read_main(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the URL shortener API!"}


def test_create_url(test_client):
    target_url = "https://www.google.com"

    response = test_client.post(
        "/url",
        json={"target_url": target_url}
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["target_url"] == target_url
    assert payload["is_active"]
    assert payload["clicks"] == 0
    assert "url" in payload
    assert "admin_url" in payload
