import logging
import typing

import structlog

from whole_app.settings import SETTINGS


def init_logger() -> None:
    our_processors: typing.Final[typing.Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]
    if SETTINGS.structured_logging:
        our_processors.append(structlog.processors.JSONRenderer())
    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        processors=our_processors,
    )
