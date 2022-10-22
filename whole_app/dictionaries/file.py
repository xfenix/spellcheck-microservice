"""Basic file provider."""
import aiopath

from whole_app.settings import SETTINGS


def init_storage() -> None:
    """Initialize dictionaries storage helper."""
    SETTINGS.dictionaries_path.mkdir(parents=True, exist_ok=True)  # pylint: disable=no-member


class FileProvider:
    """File based storage provider for user dictionaries."""

    _user_dict_path: aiopath.AsyncPath

    def prepare(self, user_name: str) -> "FileProvider":
        """Prepare class for user name."""
        self._user_dict_path = aiopath.AsyncPath(SETTINGS.dictionaries_path / user_name)
        return self

    async def _store_lines(self, lines: list[str]) -> None:
        """Store lines to user dictionary."""
        await self._user_dict_path.write_text("\n".join(lines) + "\n")

    async def save_record(self, exception_word: str) -> None:
        """Save record to user dictionary."""
        await self._user_dict_path.touch()
        clean_word: str = exception_word.strip().lower()
        file_content: list[str] = await self.fetch_records()
        if clean_word not in file_content:
            file_content.append(clean_word)
            await self._store_lines(file_content)

    async def remove_record(self, exception_word: str) -> None:
        """Remove record from user dictionary."""
        file_content: list[str] = await self.fetch_records()
        if exception_word in file_content:
            file_content.remove(exception_word)
            await self._store_lines(file_content)

    async def fetch_records(self) -> list[str]:
        """Fetch records from user dictionary."""
        if await self._user_dict_path.exists():
            return [one_line.strip() for one_line in (await self._user_dict_path.read_text()).split("\n") if one_line]
        return []
