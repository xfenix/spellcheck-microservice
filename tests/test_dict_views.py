# pylint: disable=redefined-outer-name, unspecified-encoding
"""Basic test for views."""
import importlib
import typing

import pytest
from fastapi.testclient import TestClient

from whole_app import models, views
from whole_app.settings import SETTINGS, StorageProviders

if typing.TYPE_CHECKING:
    from requests.models import Response as RequestsResponse


DICT_ENDPOINT: typing.Final[str] = f"{SETTINGS.api_prefix}/dictionaries/"


class TestFileAndDummyBasedDicts:
    """Test file based user dict provider."""

    @pytest.fixture(params=[StorageProviders.DUMMY, StorageProviders.FILE])
    def patch_various_providers(self: typing.Self, monkeypatch, request) -> typing.Any:
        """Made test, used this fixture, run for various storage providers."""
        with monkeypatch.context() as patcher:
            yield patcher.setattr(
                SETTINGS,
                "dictionaries_storage_provider",
                request.param,
            )

    @pytest.mark.repeat(3)
    def test_add_to_dict(
        self: typing.Self,
        app_client,
        faker_obj,
        patch_various_providers,  # noqa: ARG002
    ) -> None:
        """Add to user dict."""
        fake_user_name: typing.Final[str] = faker_obj.user_name()
        fake_exc_word: typing.Final[str] = faker_obj.word()
        path_to_dict_file: typing.Final[
            str
        ] = SETTINGS.dictionaries_path.joinpath(  # pylint: disable=no-member
            fake_user_name,
        )
        server_response: RequestsResponse = app_client.post(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(
                user_name=fake_user_name,
                exception_word=fake_exc_word,
            ).dict(),
        )
        assert server_response.status_code == 201
        if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
            assert fake_exc_word in path_to_dict_file.read_text()

    @pytest.mark.repeat(3)
    def test_remove_from_user_dict(
        self: typing.Self,
        app_client,
        faker_obj,
        patch_various_providers,  # noqa: ARG002
    ) -> None:
        """Delete from user dict."""
        fake_exc_word: typing.Final[str] = faker_obj.word()
        fake_user_name: typing.Final[str] = faker_obj.user_name()
        path_to_dict_file: typing.Final[
            str
        ] = SETTINGS.dictionaries_path.joinpath(  # pylint: disable=no-member
            fake_user_name,
        )
        path_to_dict_file.touch()
        path_to_dict_file.write_text(fake_exc_word)
        if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
            assert fake_exc_word in path_to_dict_file.read_text()
        server_response: RequestsResponse = app_client.delete(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(
                user_name=fake_user_name,
                exception_word=fake_exc_word,
            ).dict(),
        )
        assert server_response.status_code == 200
        if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
            assert fake_exc_word not in path_to_dict_file.read_text()

    def test_dummy_provider_init(
        self: typing.Self,
        monkeypatch,
        app_client,
        faker_obj,
    ) -> None:
        """Test init with dummy provider (through add test)."""
        monkeypatch.setattr(
            SETTINGS,
            "dictionaries_storage_provider",
            StorageProviders.DUMMY,
        )
        server_response: RequestsResponse = app_client.post(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(
                user_name=faker_obj.user_name(),
                exception_word=faker_obj.word(),
            ).dict(),
        )
        assert server_response.status_code == 201


class TestVarious:
    """Various dict api things."""

    def test_disabled_dictionary_views(self: typing.Self, monkeypatch) -> None:
        """Test views with dictionaries_disabled SETTINGS option."""
        with monkeypatch.context() as patcher:
            patcher.setattr(SETTINGS, "dictionaries_disabled", True)
            importlib.reload(views)
            server_response: RequestsResponse = TestClient(views.SPELL_APP).post(
                DICT_ENDPOINT,
                json=models.UserDictionaryRequestWithWord(
                    user_name="test",
                    exception_word="test",
                ).dict(),
            )
            assert server_response.status_code == 404
        # restore back api state to ensure other tests wont break
        importlib.reload(views)

    @pytest.mark.parametrize("api_key", [None, ""])
    def test_empty_auth_key(self: typing.Self, api_key) -> None:
        """Test add dict without api key at all."""
        server_response: RequestsResponse = TestClient(views.SPELL_APP).post(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(
                user_name="test",
                exception_word="test",
            ).dict(),
            headers={} if api_key is None else {SETTINGS.api_key_header_name: ""},
        )
        assert server_response.status_code == 403

    def test_wrong_api_key(self: typing.Self) -> None:
        """Test add dict without api key at all."""
        server_response: RequestsResponse = TestClient(views.SPELL_APP).post(
            DICT_ENDPOINT,
            json=models.UserDictionaryRequestWithWord(
                user_name="test",
                exception_word="test",
            ).dict(),
            headers={
                SETTINGS.api_key_header_name: SETTINGS.api_key
                + "wrongTrashKekJunk --- 5000",
            },
        )
        assert server_response.status_code == 401
