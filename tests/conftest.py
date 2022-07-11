"""Basic programmatic fixtures for views."""
import pathlib
import tempfile

import faker
import pytest
from fastapi.testclient import TestClient

from whole_app import views
from whole_app.settings import SETTINGS, StorageProviders


@pytest.fixture(scope="session")
def faker_obj():
    """Fixture for faker object."""
    return faker.Faker("ru_RU")


@pytest.fixture(autouse=True)
def patch_file_provider_for_temp(monkeypatch):
    """Patch settings, to rewrite dict path to temporary directory."""
    with monkeypatch.context() as patcher, tempfile.TemporaryDirectory() as tmp_dir_name:
        yield patcher.setattr(SETTINGS, "dictionaries_path", pathlib.Path(tmp_dir_name))


@pytest.fixture
def app_client(monkeypatch):
    """Fake client with patched fake storage.

    Also in a form of context manager it allow us to test startup events
    on every test.
    """
    with TestClient(views.SPELL_APP) as local_client, monkeypatch.context() as patcher:
        patcher.setattr(SETTINGS, "dictionaries_storage_provider", StorageProviders.DUMMY)
        yield local_client
