import typing

from anyio import Path as AsyncPath

from whole_app.settings import SETTINGS


def init_storage() -> None:
    SETTINGS.dictionaries_path.mkdir(
        parents=True,
        exist_ok=True,
    )


class FileProvider:
    _user_dict_path: AsyncPath

    def prepare(self: "FileProvider", user_name: str) -> "FileProvider":
        self._user_dict_path = AsyncPath(SETTINGS.dictionaries_path / user_name)
        return self

    async def _store_lines(self: "FileProvider", lines: list[str]) -> None:
        await self._user_dict_path.write_text("\n".join(lines) + "\n")

    async def save_record(self: "FileProvider", exception_word: str) -> None:
        await self._user_dict_path.touch()
        clean_word: typing.Final = exception_word.strip().lower()
        file_content: typing.Final = await self.fetch_records()
        if clean_word not in file_content:
            file_content.append(clean_word)
            await self._store_lines(file_content)

    async def remove_record(self: "FileProvider", exception_word: str) -> None:
        file_content: typing.Final = await self.fetch_records()
        if exception_word in file_content:
            file_content.remove(exception_word)
            await self._store_lines(file_content)

    async def fetch_records(self: "FileProvider") -> list[str]:
        if await self._user_dict_path.exists():
            return [one_line.strip() for one_line in (await self._user_dict_path.read_text()).split("\n") if one_line]
        return []
