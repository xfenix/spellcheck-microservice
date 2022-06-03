# pylint: disable=redefined-outer-name
"""Basic test for views."""
import random
import typing

import faker
import pytest
from fastapi.testclient import TestClient
from requests.models import Response as RequestsResponse

from whole_app import models, views
from whole_app.settings import SETTINGS


FAKER_OBJ: faker.Faker = faker.Faker("ru_RU")
RUSSIAN_LETTERS: typing.Final[str] = "абвгдежзийклмнопрстуфхцчшщъыьэюяё"


@pytest.fixture
def fake_client():
    """Fake client."""
    return TestClient(views.SPELL_APP)


@pytest.mark.parametrize("wannabe_user_input", ["Привет как дела", "Пока, я ушёл"])
def test_no_corrections(fake_client, wannabe_user_input: str):
    """Dead simple test."""
    server_response: RequestsResponse = fake_client.post(
        f"{SETTINGS.api_prefix}/check/", json=models.SpellCheckRequest(text=wannabe_user_input, language="ru").dict()
    )
    assert server_response.status_code == 200


@pytest.mark.parametrize("random_seed", range(10))
# pylint: disable=unused-argument
def test_failed_texts(fake_client, random_seed: int):
    """Not so dead simple test."""
    generated_letter: typing.Final[str] = random.choice(RUSSIAN_LETTERS)
    wannabe_user_input: str = (
        FAKER_OBJ.text().lower().replace(generated_letter, random.choice(RUSSIAN_LETTERS.replace(generated_letter, "")))
    )
    server_response: RequestsResponse = fake_client.post(
        f"{SETTINGS.api_prefix}/check/", json=models.SpellCheckRequest(text=wannabe_user_input, language="ru").dict()
    )
    assert server_response.status_code == 200


def test_healthcheck_api_good(fake_client):
    """We need to do it too."""
    server_response: RequestsResponse = fake_client.get(f"{SETTINGS.api_prefix}/health/")
    assert server_response.status_code == 200
    assert server_response.json()["version"] == "1.0.0"


def test_healthcheck_api_bad(monkeypatch, fake_client):
    """We need to do it too."""
    monkeypatch.setattr("functools.cache", lambda: "")
    monkeypatch.setattr("pathlib.Path.read_text", lambda _: "version === fucked == up == totally == 666.13.13")
    server_response: RequestsResponse = fake_client.get(f"{SETTINGS.api_prefix}/health/")
    assert server_response.status_code == 200
    assert server_response.json()["version"] == ""
