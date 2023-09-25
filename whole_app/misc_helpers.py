import sys

from loguru import logger

from .settings import SETTINGS


def init_logger() -> None:
    logger.remove()
    logger.add(sys.stdout, serialize=SETTINGS.structured_logging)
