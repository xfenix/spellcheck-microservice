import typing

import structlog

from . import dummy as dummy_storage
from . import file as file_storage
from . import protocol
from whole_app.settings import SETTINGS, StorageProviders


LOGGER_OBJ: typing.Final = structlog.get_logger()


def init_storage() -> None:
    if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
        file_storage.init_storage()
    elif SETTINGS.dictionaries_storage_provider == StorageProviders.DUMMY:
        LOGGER_OBJ.warning(
            "Storage provider set to dummy mode. "
            "Currently all user dictionary requests will be thrown away. We worn you.",
        )


def prepare_storage_engine() -> protocol.UserDictProtocol:
    if SETTINGS.dictionaries_storage_provider == StorageProviders.FILE:
        return file_storage.FileProvider()
    return dummy_storage.DummyProvider()
