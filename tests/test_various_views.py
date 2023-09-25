"""Basic test for views."""
import typing

from whole_app.settings import SETTINGS

if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_healthcheck_api_good(app_client: "TestClient") -> typing.Any:
    server_response = app_client.get(f"{SETTINGS.api_prefix}/health/")
    assert server_response.status_code == 200
    assert server_response.json()["version"] == "1.0.0"
