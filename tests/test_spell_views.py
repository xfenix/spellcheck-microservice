# pylint: disable=redefined-outer-name
import random
import typing

import pytest
from requests.models import Response as RequestsResponse

from ._fixtures import BAD_PAYLOAD
from whole_app import models
from whole_app.settings import SETTINGS, StorageProviders


if typing.TYPE_CHECKING:
    import faker
    from fastapi.testclient import TestClient


RUSSIAN_LETTERS: typing.Final = "абвгдежзийклмнопрстуфхцчшщъыьэюяё"
RU_LANG: typing.Final = "ru_RU"


@pytest.mark.parametrize(
    "wannabe_user_input",
    ["Привет как дела", "Пока, я ушёл", *BAD_PAYLOAD],
)
def test_no_corrections(app_client: "TestClient", wannabe_user_input: str) -> None:
    """Dead simple test."""
    server_response: typing.Final = app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(text=wannabe_user_input, language=RU_LANG).model_dump(),
    )
    assert server_response.status_code == 200


@pytest.mark.repeat(5)
def test_with_corrections_simple(
    app_client: "TestClient",
    faker_obj: "faker.Faker",
) -> None:
    """Not so dead simple test."""
    generated_letter: typing.Final = random.choice(RUSSIAN_LETTERS)
    wannabe_user_input: typing.Final[str] = (
        faker_obj.text()
        .lower()
        .replace(
            generated_letter,
            random.choice(RUSSIAN_LETTERS.replace(generated_letter, "")),
        )
    )
    server_response: typing.Final = app_client.post(
        f"{SETTINGS.api_prefix}/check/",
        json=models.SpellCheckRequest(
            text=wannabe_user_input,
            language=RU_LANG,
            user_name=faker_obj.user_name(),
        ).model_dump(),
    )
    assert server_response.status_code == 200


@pytest.mark.parametrize(
    ("wannabe_user_input", "tested_word"),
    [
        (BAD_PAYLOAD[0], "Капиталисиическая"),
        (BAD_PAYLOAD[1], "блохера"),
    ],
)
def test_with_exception_word_in_dictionary(
    monkeypatch: typing.Any,
    app_client: "TestClient",
    faker_obj: "faker.Faker",
    wannabe_user_input: str,
    tested_word: str,
) -> None:
    """Complex tests, where we add word to dictionary and tests that it really excluded from the output."""
    # replace all symbols from wannabe_user_input except letters and numbers
    monkeypatch.setattr(
        SETTINGS,
        "dictionaries_storage_provider",
        StorageProviders.FILE,
    )

    def run_request() -> typing.Any:
        return app_client.post(
            f"{SETTINGS.api_prefix}/check/",
            json=models.SpellCheckRequest(
                text=wannabe_user_input,
                language=RU_LANG,
                user_name=user_name,
            ).model_dump(),
        )

    def parse_words(server_response: RequestsResponse) -> typing.Any:
        return [item["word"] for item in server_response.json()["corrections"]]

    user_name: typing.Final[str] = faker_obj.user_name()
    # run usual check request
    server_response: RequestsResponse = run_request()
    assert tested_word in parse_words(server_response)
    # add word to user dictionary
    app_client.post(
        f"{SETTINGS.api_prefix}/dictionaries/",
        json=models.UserDictionaryRequestWithWord(
            user_name=user_name,
            exception_word=tested_word,
        ).model_dump(),
    )
    # and than check that excepted word not in the check output
    server_response = run_request()
    assert tested_word not in parse_words(server_response)


@pytest.mark.parametrize(
    ("wannabe_user_input", "excluded_words"),
    [("ШЯЧЛО ПОПЯЧТСА ПОПЯЧТСА", "шЯчЛо, ПоПяЧтСа")],
)
def test_default_excluded_words(
    app_client: "TestClient",
    wannabe_user_input: str,
    excluded_words: str,
    monkeypatch: typing.Any,
) -> None:
    """Dead simple test."""
    with monkeypatch.context() as patcher:
        patcher.setattr(SETTINGS, "exclusion_words", excluded_words)
        server_response: typing.Final = app_client.post(
            f"{SETTINGS.api_prefix}/check/",
            json=models.SpellCheckRequest(text=wannabe_user_input, language=RU_LANG).model_dump(),
        )
        assert server_response.status_code == 200
        assert server_response.json()["corrections"] == [], f"{server_response.json()=} --- {excluded_words=}"
