import pytest
from werkzeug.exceptions import BadRequest

from nest_client.main import encode


@pytest.mark.parametrize("body", [[1, 2], {"a": 1}, 42, "text", None])
def test_encode_ok_returns_json(make_response, body):
    assert encode(make_response(200, body)) == body


def test_encode_bad_request_raises_with_message(make_response):
    with pytest.raises(BadRequest) as excinfo:
        encode(make_response(400, text="Unknown call: Foo"))
    assert "Unknown call: Foo" in str(excinfo.value.description)
