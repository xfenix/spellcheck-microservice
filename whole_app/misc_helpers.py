"""Helper for parsing cache version."""
import sys

from loguru import logger

from .settings import SETTINGS


def init_logger() -> None:
    """Initialize logger and remove default one."""
    logger.remove()
    logger.add(sys.stdout, serialize=SETTINGS.structured_logging)
