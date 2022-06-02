"""Models for input/output."""
import typing

import pydantic


LANGUGAGE_TYPE: typing.Literal = typing.Literal["ru", "en", "de", "es", "fr", "pt"]


class OneCorrection(pydantic.BaseModel):
    """This model is one correction for one word."""

    first_position: int
    last_position: int
    word: str
    replacements: set[str]


class SpellCheckRequest(pydantic.BaseModel):
    """Request model for spell check request."""

    text: str
    language: LANGUGAGE_TYPE


class SpellCheckResponse(SpellCheckRequest):
    """This model for check response."""

    corrections: list[OneCorrection]
