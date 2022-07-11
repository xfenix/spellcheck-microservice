# pylint: disable=redefined-outer-name, unspecified-encoding
"""Basic test for views."""
import typing

import pytest
from requests.models import Response as RequestsResponse

from whole_app import models
from whole_app.settings import SETTINGS, StorageProviders


DICT_ENDPOINT: typing.Final[str] = f"{SETTINGS.api_prefix}/dictionaries/"


class TestFileUserDict:
    """Test file based user dict provider."""

    @pytest.fixture(params=[StorageProviders.DUMMY, StorageProviders.FILE])
    def _patch_various_providers(self, monkeypatch, request):
        """Made test, used this fixture, run for various storage providers."""
        with monkeypatch.context() as patcher:
            yield patcher.setattr(SETTINGS, "storage_provider", request.param)

    @pytest.mark.repeat(3)
    def test_add_to_dict(self, app_client, faker_obj, _patch_various_providers):
        """Add to user dict."""
        fake_user_name: typing.Final[str] = faker_obj.user_name()
        fake_exc_word: typing.Final[str] = faker_obj.word()
        path_to_dict_file: typing.Final[str] = SETTINGS.path_to_dictionaries.joinpath(fake_user_name)
        server_response: RequestsResponse = app_client.post(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(user_name=fake_user_name, exception_word=fake_exc_word).dict(),
        )
        assert server_response.status_code == 201
        if SETTINGS.storage_provider == StorageProviders.FILE:
            assert fake_exc_word in path_to_dict_file.read_text()

    @pytest.mark.repeat(3)
    def test_remove_from_user_dict(self, app_client, faker_obj, _patch_various_providers):
        """Delete from user dict."""
        fake_exc_word: typing.Final[str] = faker_obj.word()
        fake_user_name: typing.Final[str] = faker_obj.user_name()
        path_to_dict_file: typing.Final[str] = SETTINGS.path_to_dictionaries.joinpath(fake_user_name)
        path_to_dict_file.touch()
        path_to_dict_file.write_text(fake_exc_word)
        if SETTINGS.storage_provider == StorageProviders.FILE:
            assert fake_exc_word in path_to_dict_file.read_text()
        server_response: RequestsResponse = app_client.delete(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(user_name=fake_user_name, exception_word=fake_exc_word).dict(),
        )
        assert server_response.status_code == 200
        if SETTINGS.storage_provider == StorageProviders.FILE:
            assert fake_exc_word not in path_to_dict_file.read_text()
