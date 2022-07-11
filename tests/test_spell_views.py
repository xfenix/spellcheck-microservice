# pylint: disable=redefined-outer-name
"""Basic test for views."""
import random
import typing

import pytest
from requests.models import Response as RequestsResponse

from ._fixtures import BAD_PAYLOAD
from whole_app import models
from whole_app.settings import SETTINGS, StorageProviders


RUSSIAN_LETTERS: typing.Final[str] = "абвгдежзийклмнопрстуфхцчшщъыьэюяё"
RU_LANG: str = "ru_RU"


@pytest.mark.parametrize("wannabe_user_input", ["Привет как дела", "Пока, я ушёл", *BAD_PAYLOAD])
def test_no_corrections(app_client, wannabe_user_input):
    """Dead simple test."""
    server_response: typing.Final[RequestsResponse] = app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(text=wannabe_user_input, language=RU_LANG).dict(),
    )
    assert server_response.status_code == 200


@pytest.mark.repeat(5)
def test_with_corrections_simple(app_client, faker_obj):
    """Not so dead simple test."""
    generated_letter: typing.Final[str] = random.choice(RUSSIAN_LETTERS)
    wannabe_user_input: str = (
        faker_obj.text().lower().replace(generated_letter, random.choice(RUSSIAN_LETTERS.replace(generated_letter, "")))
    )
    server_response: typing.Final[RequestsResponse] = app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(
            text=wannabe_user_input, language=RU_LANG, user_name=faker_obj.user_name()
        ).dict(),
    )
    assert server_response.status_code == 200


@pytest.mark.parametrize("wannabe_user_input", BAD_PAYLOAD)
def test_with_exception_word_in_dictionary(monkeypatch, app_client, faker_obj, wannabe_user_input):
    """..."""
    monkeypatch.setattr(SETTINGS, "dictionaries_storage_provider", StorageProviders.FILE)
    run_request: typing.Callable = lambda: app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(text=wannabe_user_input, language=RU_LANG, user_name=user_name).dict(),
    )
    parse_words: typing.Callable = lambda server_response: [
        item["word"] for item in server_response.json()["corrections"]
    ]
    excepted_word: typing.Final[str] = wannabe_user_input.split()[0]
    user_name: typing.Final[str] = faker_obj.user_name()
    # run usual check request
    server_response: RequestsResponse = run_request()
    assert excepted_word in parse_words(server_response)
    # add word to user dictionary
    app_client.post(
        f"{SETTINGS.api_prefix}/dictionaries/",
        json=models.UserDictionaryRequestWithWord(user_name=user_name, exception_word=excepted_word).dict(),
    )
    # and than check that excepted word not in the check output
    server_response = run_request()
    print(excepted_word, parse_words(server_response))
    assert excepted_word not in parse_words(server_response)
