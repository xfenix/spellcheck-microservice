"""Basic programmatic fixtures for views."""
import pathlib
import tempfile
import typing

import faker
import pytest
from fastapi.testclient import TestClient

from whole_app import views
from whole_app.settings import SETTINGS, StorageProviders


@pytest.fixture(scope="session")
def faker_obj() -> faker.Faker:
    """Fixture for faker object."""
    return faker.Faker("ru_RU")


@pytest.fixture(autouse=True)
def patch_file_provider_for_temp(monkeypatch) -> typing.Any:
    """Patch settings, to rewrite dict path to temporary directory."""
    with monkeypatch.context() as patcher, tempfile.TemporaryDirectory() as tmp_dir_name:
        yield patcher.setattr(SETTINGS, "dictionaries_path", pathlib.Path(tmp_dir_name))


# pylint: disable=redefined-outer-name
@pytest.fixture()
def app_client(monkeypatch: typing.Any, faker_obj: typing.Any) -> typing.Any:
    """Fake client with patched fake storage.

    Also in a form of context manager it allow us to test startup events
    on every test.
    """
    fake_api_key: typing.Final[str] = faker_obj.password()
    with TestClient(views.SPELL_APP) as local_client, monkeypatch.context() as patcher:
        patcher.setattr(
            SETTINGS,
            "dictionaries_storage_provider",
            StorageProviders.DUMMY,
        )
        patcher.setattr(SETTINGS, "api_key", fake_api_key)
        local_client.headers.update({SETTINGS.api_key_header_name: fake_api_key})
        yield local_client
