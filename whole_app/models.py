# pylint: disable=no-member
"""Models for input/output."""
import typing

import pydantic

from .settings import SETTINGS, AvailableLanguages, AvailableLanguagesType


# any because mypy & pydantic cant cope with proper typing
USER_NAME_FIELDS_RESTRICTIONS: typing.Final[typing.Any] = {
    "example": "username",
    "regex": SETTINGS.username_regex,
    "min_length": SETTINGS.username_min_length,
    "max_length": SETTINGS.username_max_length,
}


class OneCorrection(pydantic.BaseModel):
    """Model with one correction for one word."""

    first_position: int
    last_position: int
    word: str
    suggestions: set[str]


class SpellCheckRequest(pydantic.BaseModel):
    """Request model for spell check request."""

    text: str = pydantic.Field(..., example="Привед как дила")
    language: AvailableLanguagesType
    user_name: str | None = pydantic.Field(**USER_NAME_FIELDS_RESTRICTIONS)


class SpellCheckResponse(pydantic.BaseModel):
    """Model for check response."""

    text: str
    language: str
    corrections: list[OneCorrection]


class UserDictionaryRequest(pydantic.BaseModel):
    """Request model for user dictionary request."""

    user_name: str = pydantic.Field(..., **USER_NAME_FIELDS_RESTRICTIONS)


class UserDictionaryRequestWithWord(UserDictionaryRequest):
    """Request model for user dictionary request with word."""

    exception_word: str = pydantic.Field(..., example="привед")


class HealthCheckResponse(pydantic.BaseModel):
    """Model for health check response."""

    service_name: str = SETTINGS.service_name
    supported_languages: tuple[str, ...] = AvailableLanguages
    version: str = SETTINGS.current_version
    status: typing.Literal["ok", "notok"] = "ok"
