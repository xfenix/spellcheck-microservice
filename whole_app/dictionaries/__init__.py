from loguru import logger

from . import dummy as dummy_storage
from . import file as file_storage
from . import protocol
from whole_app import misc_helpers
from whole_app.settings import SETTINGS, StorageProviders


misc_helpers.init_logger()


def init_storage() -> None:
    if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
        file_storage.init_storage()
    elif SETTINGS.dictionaries_storage_provider == StorageProviders.DUMMY:
        logger.warning(
            "Storage provider set to dummy mode. "
            "Currently all user dictionary requests will be thrown away. We worn you.",
        )


def prepare_storage_engine() -> protocol.UserDictProtocol:
    if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
        return file_storage.FileProvider()
    return dummy_storage.DummyProvider()
