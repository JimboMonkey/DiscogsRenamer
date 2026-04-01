from PyQt6 import QtCore
from typing import Any
from pathlib import Path

from discogsrenamer.core.constants import APP_NAME, COMPANY_NAME
from discogsrenamer.core.filename_rules import INVALID_CHARS_REPLACEMENTS

DEFAULT_SETTINGS = {
    "filename_format": "%fn - %ta - %tt",
    "zero_fill_enabled": True,
    "highlight_track_misnumbering": True,
    "initial_folder": str(Path.home()),
    "invalid_char_replacements": INVALID_CHARS_REPLACEMENTS,
}


class AppSettings:
    def __init__(self) -> None:
        self._settings = QtCore.QSettings(COMPANY_NAME, APP_NAME)

    def get(self, key: str) -> str | bool | list[tuple[str, str]]:
        default = DEFAULT_SETTINGS.get(key)

        # If the default is a bool, ask QSettings to return a bool
        if isinstance(default, bool):
            return self._settings.value(key, default, type=bool)

        return self._settings.value(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings.setValue(key, value)
        self._settings.sync()
