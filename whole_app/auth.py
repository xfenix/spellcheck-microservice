"""Basic auth via API key mechanism."""
import typing
import fastapi
from fastapi.security.api_key import APIKeyHeader

from .settings import SETTINGS


async def auth_via_api_key(
    user_provided_api_key: typing.Annotated[
        str,
        fastapi.Security(APIKeyHeader(name=SETTINGS.api_key_header_name)),
    ],
) -> str:
    """Check if api key is valid."""
    if user_provided_api_key != SETTINGS.api_key:
        raise fastapi.HTTPException(
            status_code=401,
            detail="Could not validate api key",
        )
    return user_provided_api_key
