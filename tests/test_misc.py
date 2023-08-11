# pylint: disable=no-member
"""Test __main__.py."""
import importlib
import os
import runpy
from typing import TYPE_CHECKING
import typing

from fastapi.testclient import TestClient

from whole_app import views
from whole_app.settings import SETTINGS, SettingsOfMicroservice

if TYPE_CHECKING:
    from requests.models import Response as RequestsResponse


def test_main_py(monkeypatch) -> None:
    """Test __main__.py."""

    class FakeGunicorn:
        """Fake gunicorn."""

        def __init__(self: "FakeGunicorn", *_, **__) -> None:
            """Init."""

        @property
        def cfg(self: "FakeGunicorn") -> "FakeGunicorn":
            """Fake config object."""
            return self

        @property
        def settings(self: "FakeGunicorn") -> dict[str, None | int]:
            """Fake settings object."""
            return {
                "bind": None,
                "workers": 666_13,
            }

        def set(self: "FakeGunicorn", _, __) -> typing.Any:  # noqa: A003
            """Fake setter for «config» object."""

        def run(self: "FakeGunicorn", *_, **__) -> typing.Any:
            """Faky run."""
            self.load_config()
            self.load()

    monkeypatch.setattr("gunicorn.app.base.BaseApplication", FakeGunicorn)
    runpy.run_module("whole_app.__main__", run_name="__main__")


def test_incorrect_settings(monkeypatch) -> None:
    """Test some various incorrect settings."""
    fake_settings: SettingsOfMicroservice = SettingsOfMicroservice()
    assert fake_settings.cache_size == 10_000

    os.environ["SPELLCHECK_CACHE_SIZE"] = "-666"

    monkeypatch.setattr(
        "pathlib.Path.read_text",
        lambda _: "version === fucked == up == totally == 666.13.13",
    )
    fake_settings = SettingsOfMicroservice()
    assert fake_settings.cache_size == 0
    assert fake_settings.current_version == ""


def test_sentry_integration(monkeypatch, faker_obj) -> None:
    """Test sentry integration."""
    with monkeypatch.context() as patcher:
        patcher.setattr(SETTINGS, "sentry_dsn", f"https://{faker_obj.pystr()}")
        patcher.setattr("sentry_sdk.init", lambda **_: None)
        importlib.reload(views)
        server_response: RequestsResponse = TestClient(views.SPELL_APP).get(
            f"{SETTINGS.api_prefix}/health/",
        )
        assert server_response.status_code == 200
    # restore back api state to ensure other tests wont break
    importlib.reload(views)
