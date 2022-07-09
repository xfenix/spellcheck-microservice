# pylint: disable=no-member, no-self-argument
"""Core settings of whole project."""
import pathlib

import pydantic


class _SettingsWrapperWhoseNameNobodyCaresAbout(pydantic.BaseSettings):
    """Literally no one cares."""

    service_name: str = "spellcheck-microservice"
    debug: bool = True
    structured_logging: bool = True
    workers: int = 8
    port: int = 10_113
    cache_size: int = 10_000
    api_prefix: str = "/api/"
    docs_url: str = "/docs/"
    max_suggestions: pydantic.conint(gt=0) | None = None  # type: ignore
    path_to_version_file = pathlib.Path(__file__).parent.parent / "pyproject.toml"

    @pydantic.validator("api_prefix")
    def api_prefix_must_be_with_slash_for_left_part_and_without_it_for_right(cls, possible_value: str) -> str:
        """Helps not mess up the API prefix in the application.."""
        return f"/{possible_value.strip('/')}"

    class Config:
        """I hate this config classes in classes."""

        env_prefix: str = "spellcheck_microservice_"


SETTINGS: _SettingsWrapperWhoseNameNobodyCaresAbout = _SettingsWrapperWhoseNameNobodyCaresAbout()
