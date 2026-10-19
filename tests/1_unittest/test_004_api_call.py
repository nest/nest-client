import pytest
from werkzeug.exceptions import BadRequest

from nest_client.main import default_url


def test_api_call_without_arguments(client):
    assert client.api_call("ResetKernel") == [1, 2, 3]
    client.session.post.assert_called_once_with(f"{default_url}/api/ResetKernel", json={"args": []})


def test_api_call_with_args_and_kwargs(client):
    client.api_call("Create", ("iaf_psc_alpha",), {"n": 2})
    client.session.post.assert_called_once_with(f"{default_url}/api/Create", json={"n": 2, "args": ("iaf_psc_alpha",)})


def test_api_call_raises_bad_request(client, make_response):
    client.session.post.return_value = make_response(400, text="error")
    with pytest.raises(BadRequest):
        client.api_call("Foo")
