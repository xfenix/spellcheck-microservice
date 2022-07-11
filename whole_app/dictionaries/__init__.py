"""Initalizatior of user dictionaries."""
import typing

from loguru import logger

from . import dummy as dummy_storage
from . import file as file_storage
from . import protocol
from whole_app import misc_helpers
from whole_app.settings import SETTINGS, StorageProviders


misc_helpers.init_logger()


def init_storage() -> typing.Any:
    """Generic storage initializer."""
    match SETTINGS.dictionaries_storage_provider:
        case StorageProviders.FILE:
            return file_storage.init_storage()
        case StorageProviders.DUMMY:
            logger.warning(
                "Storage provider set to dummy mode. "
                "Currently all user dictionary requests will be thrown away. We worn you."
            )
            return None


def prepare_storage_engine() -> protocol.UserDictProtocol:
    """Storage engine factory."""
    match SETTINGS.dictionaries_storage_provider:
        case StorageProviders.FILE:
            return file_storage.FileProvider()
        case StorageProviders.DUMMY:
            return dummy_storage.DummyProvider()
