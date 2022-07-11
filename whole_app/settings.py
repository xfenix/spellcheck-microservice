# pylint: disable=no-member, no-self-argument
"""Core settings of whole project."""
import enum
import pathlib
import typing

import pydantic
from loguru import logger


AvailableLanguagesType = typing.Literal["ru_RU", "en_US", "es_ES", "fr_FR", "de_DE", "pt_PT"]
AvailableLanguages: tuple[str, ...] = typing.get_args(AvailableLanguagesType)


class StorageProviders(enum.Enum):
    """Default system storage providers."""

    FILE: str = "file"
    DUMMY: str = "dummy"


class SettingsOfMicroservice(pydantic.BaseSettings):
    """Literally no one cares."""

    api_key: str = "DefaultAPIKEYValue1"
    service_name: str = "spellcheck-microservice"
    enable_cors: bool = True
    structured_logging: bool = True
    workers: pydantic.conint(gt=0, lt=301) = 8  # type: ignore
    port: pydantic.conint(gt=1_023, lt=65_536) = 10_113  # type: ignore
    cache_size: int = 10_000
    api_prefix: str = "/api/"
    docs_url: str = "/docs/"
    max_suggestions: pydantic.conint(gt=0) | None = None  # type: ignore
    # version from this file will be available in the health check response
    # and version in the file itself will be updated in the CI through poetry version command
    path_to_version_file: pathlib.Path = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    dictionaries_path: pathlib.Path = pathlib.Path("/data/")
    dictionaries_storage_provider: StorageProviders = StorageProviders.FILE
    dictionaries_disabled: bool = False

    @pydantic.validator("api_prefix")
    def api_prefix_must_be_with_slash_for_left_part_and_without_it_for_right(cls, possible_value: str) -> str:
        """Helps not mess up the API prefix in the application.."""
        return f"/{possible_value.strip('/')}"

    @pydantic.validator("cache_size")
    def warn_about_poor_lru_cache_size(cls, possible_value: int) -> int:
        """Warn about poor LRU cache size."""
        if possible_value < 1:
            logger.warning(
                "You set cache size less then 1. In this case, the cache size will be unlimited and polute your memory."
            )
        return possible_value

    class Config:
        """I hate this config classes in classes."""

        env_prefix: str = "spellcheck_"


SETTINGS: SettingsOfMicroservice = SettingsOfMicroservice()
