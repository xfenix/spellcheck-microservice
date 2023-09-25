# pylint: disable=no-member
"""Models for input/output."""
import typing

import pydantic

from .settings import SETTINGS, AvailableLanguages, AvailableLanguagesType


class _RequestWithUserName(pydantic.BaseModel):
    user_name: str | None = pydantic.Field(
        example="username",
        regex=SETTINGS.username_regex,
        min_length=SETTINGS.username_min_length,
        max_length=SETTINGS.username_max_length,
    )


class OneCorrection(pydantic.BaseModel):
    first_position: int
    last_position: int
    word: str
    suggestions: set[str]


class SpellCheckRequest(_RequestWithUserName):
    text: str = pydantic.Field(..., example="Привед как дила")
    language: AvailableLanguagesType


class SpellCheckResponse(pydantic.BaseModel):
    text: str
    language: str
    corrections: list[OneCorrection]


class UserDictionaryRequest(_RequestWithUserName):
    pass


class UserDictionaryRequestWithWord(UserDictionaryRequest):
    exception_word: str = pydantic.Field(..., example="привед")


class HealthCheckResponse(pydantic.BaseModel):
    service_name: str = SETTINGS.service_name
    supported_languages: tuple[str, ...] = AvailableLanguages
    version: str = SETTINGS.current_version
    status: typing.Literal["ok", "notok"] = "ok"
