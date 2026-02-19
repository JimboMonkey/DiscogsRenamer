from PyQt6 import QtCore
from typing import Any

from constants import APP_NAME
from filename_rules import INVALID_CHARS_REPLACEMENTS

DEFAULT_SETTINGS = {
    "filename_format": "%fn - %ta - %tt",
    "zero_fill_enabled": True,
    "invalid_char_replacements": INVALID_CHARS_REPLACEMENTS,
}


class AppSettings:
    def __init__(self):
        self._settings = QtCore.QSettings("Jimbomonkey Productions", APP_NAME)

    def get(self, key: str):
        default = DEFAULT_SETTINGS.get(key)

        # If the default is a bool, ask QSettings to return a bool
        if isinstance(default, bool):
            return self._settings.value(key, default, type=bool)

        return self._settings.value(key, default)

    def set(self, key: str, value: Any):
        self._settings.setValue(key, value)
        self._settings.sync()
