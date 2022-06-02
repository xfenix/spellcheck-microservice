"""Models for input/output."""
import typing

import pydantic


class OneCorrection(pydantic.BaseModel):
    """This model is one correction for one word."""

    first_position: int
    last_position: int
    word: str
    replacements: set[str]


class SpellCheckRequest(pydantic.BaseModel):
    """Request model for spell check request."""

    text: str = pydantic.Field(..., example="Привед как дила")
    language: typing.Literal["ru", "en", "de", "es", "fr", "pt"]


class SpellCheckResponse(SpellCheckRequest):
    """This model for check response."""

    corrections: list[OneCorrection]
