import requests

from nest_client import NESTClient
from nest_client.main import default_headers, default_url


def test_init_defaults():
    client = NESTClient()
    assert client.url == default_url
    assert client.state == {}
    assert isinstance(client.session, requests.Session)
    for key, value in default_headers.items():
        assert client.session.headers[key] == value


def test_init_custom_url_and_headers():
    client = NESTClient(url="http://example.test:1234", headers={"Authorization": "Bearer xyz"})
    assert client.url == "http://example.test:1234"
    assert client.session.headers["Authorization"] == "Bearer xyz"
    # Default headers are kept.
    assert client.session.headers["Content-type"] == "application/json"


def test_init_custom_headers_override_defaults():
    client = NESTClient(headers={"Accept": "application/json"})
    assert client.session.headers["Accept"] == "application/json"


def test_init_does_not_mutate_default_headers():
    before = dict(default_headers)
    NESTClient(headers={"X-Test": "1"})
    assert default_headers == before


def test_clients_have_independent_state_and_sessions():
    a, b = NESTClient(), NESTClient()
    a.state["x"] = 1
    assert b.state == {}
    assert a.session is not b.session
