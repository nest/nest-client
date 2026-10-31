from nest_client.main import default_url


def test_get_prefixes_url_and_forwards_arguments(client):
    response = client.get("/", timeout=5)
    client.session.get.assert_called_once_with(f"{default_url}/", timeout=5)
    assert response.json() == {"ok": True}


def test_post_prefixes_url_and_forwards_arguments(client):
    client.post("/api/Foo", json={"a": 1})
    client.session.post.assert_called_once_with(f"{default_url}/api/Foo", json={"a": 1})
