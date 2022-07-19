"""Basic test for views."""
from requests.models import Response

from whole_app.settings import SETTINGS


def test_healthcheck_api_good(app_client):
    """Basic healthcheck test."""
    server_response: Response = app_client.get(f"{SETTINGS.api_prefix}/health/")
    assert server_response.status_code == 200
    assert server_response.json()["version"] == "1.0.0"
