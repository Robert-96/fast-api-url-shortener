
def post_url(test_client, target_url):
    return test_client.post(
        "/url",
        json={"target_url": target_url}
    )


def peek_url(test_client, url_key):
    return test_client.get(f"/peek/{url_key}")


def test_index(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the URL shortener API!"}


def test_create_url(test_client):
    target_url = "https://www.google.com"

    response = post_url(test_client, target_url)
    payload = response.json()

    assert response.status_code == 200
    assert payload["target_url"] == target_url
    assert payload["is_active"]
    assert payload["clicks"] == 0
    assert "url" in payload
    assert "admin_url" in payload


def test_peek(test_client):
    target_url = "https://www.google.com"
    response = post_url(test_client, target_url)
    assert response.status_code == 200
    payload = response.json()
    url_key = payload["key"]

    response = peek_url(test_client, url_key)

    assert response.status_code == 200
    assert payload["target_url"] == target_url
    assert payload["is_active"]
    assert payload["clicks"] == 0
    assert "url" in payload


def test_peek_with_inexistent_url(test_client):
    response = peek_url(test_client, "NOT-APPLICABLE")

    assert response.status_code == 404


def test_forward_target(test_client):
    target_url = "https://www.google.com"
    post_response = post_url(test_client, target_url)
    assert post_response.status_code == 200
    post_payload = post_response.json()
    url_key = post_payload["key"]

    redirect_response = test_client.get(
        f"/{url_key}",
        follow_redirects=False
    )

    assert redirect_response.status_code == 307
    peek_response = peek_url(test_client, url_key)
    assert peek_response.status_code == 200
    peek_payload = peek_response.json()
    assert peek_payload["clicks"] == 1


def test_forward_target_with_inexistent_url(test_client):
    redirect_response = test_client.get(
        "/NOT-APPLICABLE",
        follow_redirects=False
    )

    assert redirect_response.status_code == 404


def test_get_admin_info(test_client):
    target_url = "https://www.google.com"
    response = post_url(test_client, target_url)
    assert response.status_code == 200
    payload = response.json()
    secret_key = payload["secret_key"]

    admin_response = test_client.get(f"/admin/{secret_key}")

    assert admin_response.status_code == 200


def test_get_admin_info_with_inexistent_url(test_client):
    admin_response = test_client.get(f"/admin/NOT-APPLICABLE")

    assert admin_response.status_code == 404


def test_delete_url(test_client):
    target_url = "https://www.google.com"
    response = post_url(test_client, target_url)
    assert response.status_code == 200
    payload = response.json()
    url_key = payload["key"]
    secret_key = payload["secret_key"]

    peek_response = peek_url(test_client, url_key)
    assert peek_response.status_code == 200

    delete_response = test_client.delete(f"/admin/{secret_key}")
    assert delete_response.status_code == 200

    peek_response = peek_url(test_client, url_key)
    assert peek_response.status_code == 404


def test_delete_url_for_inexistent_url(test_client):
    delete_response = test_client.delete("/admin/NOT-APPLICABLE")

    assert delete_response.status_code == 404
