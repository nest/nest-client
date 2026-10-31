import pytest

from nest_client.main import default_url


@pytest.mark.parametrize("as_str", [True, False])
def test_from_file_sends_file_content(client, tmp_path, capsys, as_str):
    source = "import nest\nn = nest.Create('iaf_psc_alpha')\n"
    path = tmp_path / "script.py"
    path.write_text(source)

    client.from_file(str(path) if as_str else path, ["n"])

    client.session.post.assert_called_once_with(
        f"{default_url}/exec", json={"source": source, "return": ["n"], "return_vars": ["n"]}
    )
    out = capsys.readouterr().out
    assert str(path) in out
    assert source in out


def test_from_file_missing_file_raises(client, tmp_path):
    with pytest.raises(FileNotFoundError):
        client.from_file(tmp_path / "missing.py")
    client.session.post.assert_not_called()
