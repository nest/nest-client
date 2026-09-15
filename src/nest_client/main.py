# main.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import Callable
from pathlib import Path

import requests
from werkzeug.exceptions import BadRequest

__all__ = [
    "NESTClient",
]

default_url = "http://localhost:52425"
default_headers = {"Content-type": "application/json", "Accept": "text/plain"}


def encode(response):
    if response.ok:
        return response.json()
    elif response.status_code == 400:
        raise BadRequest(response.text)


class NESTClient:
    def __init__(self, url: str = default_url, headers: dict = default_headers):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({**default_headers, **headers})
        self.state = {}

    def get(self, path: str, *args, **kwargs):
        return self.session.get(f"{self.url}{path}", *args, **kwargs)

    def post(self, path: str, *args, **kwargs):
        return self.session.post(f"{self.url}{path}", *args, **kwargs)

    def __getattr__(self, call: str) -> Callable:
        def method(*args, **kwargs):
            return self.api_call(call, args, kwargs)

        return method

    def api_call(self, call: str, args: list | tuple | None = None, kwargs: dict | None = None):

        if args is None:
            args = []

        if kwargs is None:
            kwargs = {}

        kwargs.update({"args": args})
        response = self.post(f"/api/{call}", json=kwargs)
        return encode(response)

    def exec_script(self, source: str, return_vars: str | list[str] | None = None):
        params = {
            "source": source,
            "return": return_vars,
            "return_vars": return_vars,
        }
        response = self.post("/exec", json=params)
        return encode(response)

    def from_file(self, filename: Path | str, return_vars: str | list[str] | None = None):
        with open(filename) as f:
            lines = f.readlines()
        script = "".join(lines)

        print(f"Execute script code of {filename}")
        print(f"Return variables: {return_vars}")
        print(20 * "-")
        print(script)
        print(20 * "-")

        return self.exec_script(script, return_vars)
