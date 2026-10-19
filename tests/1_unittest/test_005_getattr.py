from nest_client.main import default_url


def test_getattr_returns_callable_for_unknown_attribute(client):
    assert callable(client.SomeNestFunction)
    client.session.post.assert_not_called()


def test_getattr_dispatches_to_api_call(client):
    result = client.Create("iaf_psc_alpha", n=10, params={"I_e": 376.0})
    assert result == [1, 2, 3]
    client.session.post.assert_called_once_with(
        f"{default_url}/api/Create",
        json={"n": 10, "params": {"I_e": 376.0}, "args": ("iaf_psc_alpha",)},
    )


def test_getattr_does_not_shadow_real_attributes(client):
    assert client.url == default_url
    assert isinstance(client.state, dict)
    client.session.post.assert_not_called()
