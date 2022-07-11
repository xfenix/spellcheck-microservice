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
    match SETTINGS.storage_provider:
        case StorageProviders.FILE:
            return file_storage.init_storage()
        case StorageProviders.DUMMY:
            logger.warning(
                "Storage provider set to None mode. Currently all user dictionary requests will be thrown away."
                "We worn you"
            )
            return None
        case _:
            raise NotImplementedError("Storage provider is not implemented")


def prepare_storage_engine() -> protocol.UserDictProtocol:
    """Storage engine factory."""
    match SETTINGS.storage_provider:
        case StorageProviders.FILE:
            return file_storage.FileProvider()
        case StorageProviders.DUMMY:
            return dummy_storage.DummyProvider()
        case _:
            raise NotImplementedError("Storage provider is not implemented")
