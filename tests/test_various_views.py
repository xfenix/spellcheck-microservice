import typing

import toml

from whole_app.settings import PATH_TO_PYPROJECT, SETTINGS


if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_healthcheck_api_good(app_client: "TestClient") -> typing.Any:
    server_response = app_client.get(f"{SETTINGS.api_prefix}/health/")
    assert server_response.status_code == 200
    assert server_response.json()["version"] == toml.loads(PATH_TO_PYPROJECT.read_text())["tool"]["poetry"]["version"]
