import importlib
import os
import runpy
import typing

from fastapi.testclient import TestClient
from granian.constants import Interfaces

from whole_app import views
from whole_app.settings import SETTINGS, SettingsOfMicroservice


if typing.TYPE_CHECKING:
    import faker


def test_main_py(monkeypatch: typing.Any) -> None:
    captured_parameters: dict[str, typing.Any] = {}

    class FakeGranian:
        def __init__(
            self: "FakeGranian",
            target: str,
            *,
            address: str,
            port: int,
            workers: int,
            interface: Interfaces,
        ) -> None:
            captured_parameters.update(
                {
                    "target": target,
                    "address": address,
                    "port": port,
                    "workers": workers,
                    "interface": interface,
                },
            )

        def serve(self: "FakeGranian") -> None:
            captured_parameters["served"] = True

    monkeypatch.setattr("granian.Granian", FakeGranian)
    runpy.run_module("whole_app.__main__", run_name="__main__")

    assert captured_parameters == {
        "target": "whole_app.views:SPELL_APP",
        "address": SETTINGS.server_address,
        "port": SETTINGS.port,
        "workers": SETTINGS.workers,
        "interface": Interfaces.ASGI,
        "served": True,
    }


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
