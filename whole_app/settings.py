"""Core settings of whole project."""
import pathlib

import pydantic


class _SettingsWrapperWhoseNameNobodyCaresAbout(pydantic.BaseSettings):
    """Literally no one cares."""

    service_name: str = "spellcheck-microservice"
    debug: bool = True
    structured_logging: bool = True
    workers: int = 4
    port: int = 10113
    api_prefix: str = "/api/"
    docs_url: str = "/docs/"
    path_to_version_file = pathlib.Path(__file__).parent.parent / "pyproject.toml"

    @pydantic.validator("api_prefix")
    # pylint: disable=no-self-argument
    def api_prefix_must_be_with_slash_for_left_part_and_without_it_for_right(cls, possible_value: str) -> str:
        """Helps not mess up the API prefix in the application.."""
        return f"/{possible_value.strip('/')}"

    class Config:
        """I hate this config classes in classes."""

        env_prefix: str = "spellcheck_microservice_"


SETTINGS: _SettingsWrapperWhoseNameNobodyCaresAbout = _SettingsWrapperWhoseNameNobodyCaresAbout()
