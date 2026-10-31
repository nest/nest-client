import pytest
from werkzeug.exceptions import BadRequest

from nest_client.main import default_url


def test_exec_script_with_return_vars(client, make_response):
    client.session.post.return_value = make_response(body={"data": {"n": 1}})
    assert client.exec_script("n = 1", "n") == {"data": {"n": 1}}
    client.session.post.assert_called_once_with(
        f"{default_url}/exec", json={"source": "n = 1", "return": "n", "return_vars": "n"}
    )


def test_exec_script_without_return_vars(client):
    client.exec_script("import nest")
    client.session.post.assert_called_once_with(
        f"{default_url}/exec", json={"source": "import nest", "return": None, "return_vars": None}
    )


def test_exec_script_raises_bad_request(client, make_response):
    client.session.post.return_value = make_response(400, text="SyntaxError")
    with pytest.raises(BadRequest):
        client.exec_script("this is not python")
