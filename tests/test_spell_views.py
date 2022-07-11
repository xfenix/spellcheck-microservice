# pylint: disable=redefined-outer-name
"""Basic test for views."""
import random
import typing

import pytest
from requests.models import Response as RequestsResponse

from ._fixtures import BAD_PAYLOAD
from whole_app import models
from whole_app.settings import SETTINGS


RUSSIAN_LETTERS: typing.Final[str] = "абвгдежзийклмнопрстуфхцчшщъыьэюяё"
RU_LANG: str = "ru_RU"


@pytest.mark.parametrize("wannabe_user_input", ["Привет как дела", "Пока, я ушёл", *BAD_PAYLOAD])
def test_no_corrections(app_client, wannabe_user_input):
    """Dead simple test."""
    server_response: RequestsResponse = app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(text=wannabe_user_input, language=RU_LANG).dict(),
    )
    assert server_response.status_code == 200


@pytest.mark.repeat(10)
def test_with_corrections(app_client, faker_obj):
    """Not so dead simple test."""
    generated_letter: typing.Final[str] = random.choice(RUSSIAN_LETTERS)
    wannabe_user_input: str = (
        faker_obj.text().lower().replace(generated_letter, random.choice(RUSSIAN_LETTERS.replace(generated_letter, "")))
    )
    server_response: RequestsResponse = app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(
            text=wannabe_user_input, language=RU_LANG, user_name=faker_obj.user_name()
        ).dict(),
    )
    assert server_response.status_code == 200
