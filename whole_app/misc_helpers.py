"""Helper for parsing cache version."""
import sys

from loguru import logger

from .settings import SETTINGS


def setup_logger() -> None:
    """Config logger."""
    logger.add(sys.stdout, serialize=SETTINGS.structured_logging)


def parse_version_from_local_file() -> str:
    """Parse version from version file."""
    pyproject_lines: list[str] = SETTINGS.path_to_version_file.read_text().split("\n")
    version_parts: list[str] = []
    for one_line in pyproject_lines:
        if "version" in one_line:
            version_parts = one_line.split("=")
            break
    if len(version_parts) == 2:
        return version_parts[1].strip().strip('"')
    logger.warning("Can't parse version from pyproject.toml")
    return ""
