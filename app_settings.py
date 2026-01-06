from PyQt6 import QtCore
from typing import Any

from constants import APP_NAME


class AppSettings:
    def __init__(self):
        self._settings = QtCore.QSettings("Jimbomonkey Productions", APP_NAME)

    def get(self, key: str):
        return self._settings.value(key)

    def set(self, key: str, value: Any):
        self._settings.setValue(key, value)
        self._settings.sync()
