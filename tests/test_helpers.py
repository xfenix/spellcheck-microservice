# pylint: disable=redefined-outer-name
"""Additional tests."""

import faker

from whole_app.misc_helpers import parse_version_from_local_file


FAKER_OBJ: faker.Faker = faker.Faker("ru_RU")


def test_bad_parse_version_from_local_file(monkeypatch):
    """We need to do it too."""
    monkeypatch.setattr("pathlib.Path.read_text", lambda _: "version === fucked == up == totally == 666.13.13")
    assert parse_version_from_local_file() == ""
