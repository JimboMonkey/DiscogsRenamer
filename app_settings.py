from PyQt6 import QtCore

from constants import APP_NAME


class AppSettings:
    def __init__(self):
        self._settings = QtCore.QSettings("Jimbomonkey Productions", APP_NAME)

    def get(self, key: str):
        return self._settings.value(key)

    def set(self, key: str, value: str | bool):
        self._settings.setValue(key, value)
        self._settings.sync()
