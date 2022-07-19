# pylint: disable=no-member
"""Test __main__.py."""
import importlib
import os
import runpy

from fastapi.testclient import TestClient
from requests.models import Response as RequestsResponse

from whole_app import views
from whole_app.settings import SETTINGS, SettingsOfMicroservice


def test_main_py(monkeypatch):
    """Test __main__.py."""

    class FakeGunicorn:
        """Fake gunicorn."""

        def __init__(self, *_, **__):
            """Init."""

        @property
        def cfg(self):
            """Fake config object."""
            return self

        @property
        def settings(self):
            """Fake settings object."""
            return {
                "bind": None,
                "workers": 666_13,
            }

        def set(self, _, __):
            """Fake setter for «config» object."""

        def run(self, *_, **__):
            """Faky run."""
            self.load_config()
            self.load()

    monkeypatch.setattr("gunicorn.app.base.BaseApplication", FakeGunicorn)
    runpy.run_module("whole_app.__main__", run_name="__main__")


def test_incorrect_settings(monkeypatch):
    """Test some various incorrect settings."""
    fake_settings: SettingsOfMicroservice = SettingsOfMicroservice()
    assert fake_settings.cache_size == 10_000

    os.environ["SPELLCHECK_CACHE_SIZE"] = "-666"

    monkeypatch.setattr("pathlib.Path.read_text", lambda _: "version === fucked == up == totally == 666.13.13")
    fake_settings = SettingsOfMicroservice()
    assert fake_settings.cache_size == 0
    assert fake_settings.current_version == ""


def test_sentry_integration(monkeypatch, faker_obj):
    """Test sentry integration."""
    with monkeypatch.context() as patcher:
        patcher.setattr(SETTINGS, "sentry_dsn", f"https://{faker_obj.pystr()}")
        patcher.setattr("sentry_sdk.init", lambda **_: None)
        importlib.reload(views)
        server_response: RequestsResponse = TestClient(views.SPELL_APP).get(f"{SETTINGS.api_prefix}/health/")
        assert server_response.status_code == 200
    # restore back api state to ensure other tests wont break
    importlib.reload(views)
