"""Helper for parsing cache version."""
import sys

import toml
from loguru import logger

from .settings import SETTINGS


logger.add(sys.stdout, serialize=SETTINGS.structured_logging)


def parse_version_from_local_file() -> str:
    """Parse version from version file."""
    try:
        pyproject_obj: dict = toml.loads(SETTINGS.path_to_version_file.read_text())
        return pyproject_obj["tool"]["poetry"]["version"]
    except (toml.TomlDecodeError, KeyError) as exc:
        logger.warning(f"Cant parse version from pyproject. Trouble {exc}")
        return ""
