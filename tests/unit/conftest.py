"""Fixtures for unit tests of nest_client which do not require a running NEST Server.

All HTTP traffic is intercepted by replacing ``requests.Session.get/post`` with mocks.
"""

import json
from collections.abc import Callable
from unittest import mock

import pytest
import requests

from nest_client import NESTClient


def _make_response(status_code: int = 200, body=None, text: str | None = None) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    if text is None:
        text = json.dumps(body)
    response._content = text.encode()
    return response


@pytest.fixture
def make_response() -> Callable[..., requests.Response]:
    return _make_response


@pytest.fixture
def client() -> NESTClient:
    client = NESTClient()
    client.session.get = mock.Mock(return_value=_make_response(body={"ok": True}))
    client.session.post = mock.Mock(return_value=_make_response(body=[1, 2, 3]))
    return client
