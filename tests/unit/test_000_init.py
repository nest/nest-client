import importlib
from importlib import metadata

import nest_client


def test_version_matches_metadata():
    assert nest_client.__version__ == metadata.version("nest-client")


def test_metadata_not_exported():
    assert not hasattr(nest_client, "metadata")


def test_version_fallback(monkeypatch):
    def fake_version(name):
        raise metadata.PackageNotFoundError(name)

    monkeypatch.setattr(metadata, "version", fake_version)
    try:
        importlib.reload(nest_client)
        assert nest_client.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(nest_client)
