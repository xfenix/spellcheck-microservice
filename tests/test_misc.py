import importlib
import os
import runpy
import typing
from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

from whole_app import views
from whole_app.settings import SETTINGS, SettingsOfMicroservice


if TYPE_CHECKING:
    import faker


def test_main_py(monkeypatch: typing.Any) -> None:
    class FakeGunicorn:
        def __init__(self: "FakeGunicorn", *_: typing.Any, **__: typing.Any) -> None:
            """Init."""

        @property
        def cfg(self: "FakeGunicorn") -> "FakeGunicorn":
            return self

        @property
        def settings(self: "FakeGunicorn") -> dict[str, None | int]:
            return {
                "bind": None,
                "workers": 666_13,
            }

        def set(  # noqa: A003
            self: "FakeGunicorn",
            _: typing.Any,
            __: typing.Any,
        ) -> typing.Any:
            """Fake setter for «config» object."""

        def load_config(self: "FakeGunicorn") -> None:
            pass

        def load(self: "FakeGunicorn") -> None:
            pass

        def run(self: "FakeGunicorn", *_: typing.Any, **__: typing.Any) -> typing.Any:
            self.load_config()
            self.load()

    monkeypatch.setattr("gunicorn.app.base.BaseApplication", FakeGunicorn)
    runpy.run_module("whole_app.__main__", run_name="__main__")


def test_incorrect_settings(monkeypatch: typing.Any) -> None:
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


def test_sentry_integration(monkeypatch: typing.Any, faker_obj: "faker.Faker") -> None:
    with monkeypatch.context() as patcher:
        patcher.setattr(SETTINGS, "sentry_dsn", f"https://{faker_obj.pystr()}")
        patcher.setattr("sentry_sdk.init", lambda **_: None)
        importlib.reload(views)
        server_response = TestClient(views.SPELL_APP).get(
            f"{SETTINGS.api_prefix}/health/",
        )
        assert server_response.status_code == 200
    # restore back api state to ensure other tests wont break
    importlib.reload(views)
