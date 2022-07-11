"""All projects end-points lie here."""
import typing

import fastapi
from anyio import to_thread
from fastapi.middleware.cors import CORSMiddleware

from . import dictionaries, misc_helpers, models, spell
from .auth import auth_via_api_key
from .dictionaries.protocol import UserDictProtocol
from .settings import SETTINGS


SPELL_APP: typing.Final[fastapi.FastAPI] = fastapi.FastAPI(
    title=SETTINGS.app_title,
    version=SETTINGS.current_version,
    docs_url=SETTINGS.docs_url,
    openapi_url=f"{SETTINGS.api_prefix}/openapi.json",
)
if SETTINGS.enable_cors:
    SPELL_APP.add_middleware(
        CORSMiddleware,
        allow_origins=("*",),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@SPELL_APP.on_event("startup")
def startup() -> None:
    """Initialize storage."""
    dictionaries.init_storage()
    misc_helpers.init_logger()


@SPELL_APP.post(f"{SETTINGS.api_prefix}/check/", summary="Check spelling")
async def spell_check_main_endpoint(
    request_payload: models.SpellCheckRequest,
    spell_service: spell.SpellCheckService = fastapi.Depends(),
    storage_engine: UserDictProtocol = fastapi.Depends(dictionaries.prepare_storage_engine),
) -> models.SpellCheckResponse:
    """Check spelling of text for exact language."""
    exclusion_words: list[str] = []
    if request_payload.user_name and not SETTINGS.dictionaries_disabled:
        exclusion_words = await storage_engine.prepare(request_payload.user_name).fetch_records()
    return models.SpellCheckResponse(
        **request_payload.dict(),
        corrections=await to_thread.run_sync(spell_service.prepare(request_payload, exclusion_words).run_check),
    )


@SPELL_APP.get(f"{SETTINGS.api_prefix}/health/", summary="Regular healthcheck api")
async def check_health_of_service() -> models.HealthCheckResponse:
    """Check health of service."""
    return models.HealthCheckResponse()


if not SETTINGS.dictionaries_disabled:

    @SPELL_APP.post(
        f"{SETTINGS.api_prefix}/dictionaries/",
        summary="Add word to user dictionary",
        status_code=201,
    )
    async def save_word(
        request_model: models.UserDictionaryRequestWithWord,
        storage_engine: UserDictProtocol = fastapi.Depends(dictionaries.prepare_storage_engine),
        _: str = fastapi.Depends(auth_via_api_key),
    ) -> bool:
        """Save word to user dictionary."""
        await storage_engine.prepare(request_model.user_name).save_record(request_model.exception_word)
        return True

    @SPELL_APP.delete(
        f"{SETTINGS.api_prefix}/dictionaries/",
        summary="Remove word from user dictionary",
    )
    async def delete_word(
        request_model: models.UserDictionaryRequestWithWord,
        storage_engine: UserDictProtocol = fastapi.Depends(dictionaries.prepare_storage_engine),
        _: str = fastapi.Depends(auth_via_api_key),
    ) -> bool:
        """Save word to user dictionary."""
        await storage_engine.prepare(request_model.user_name).remove_record(request_model.exception_word)
        return True
