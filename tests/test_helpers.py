# pylint: disable=redefined-outer-name
"""Additional tests."""
from whole_app.misc_helpers import parse_version_from_local_file


def test_bad_parse_version_from_local_file(monkeypatch):
    """We need to do it too."""
    monkeypatch.setattr("functools.cache", lambda _: _)
    monkeypatch.setattr("pathlib.Path.read_text", lambda _: "version === fucked == up == totally == 666.13.13")
    assert parse_version_from_local_file() == ""
