from pytestqt.qtbot import QtBot
from typing import Any

from gui.dialogs.settings_dialog import SettingsDialog
from core.app_settings import DEFAULT_SETTINGS


class FakeSettings:
    def __init__(self) -> None:
        self._store = {}

    def get(self, key: str) -> str | bool | list[tuple[str, str]]:
        default = DEFAULT_SETTINGS.get(key)

        # If the default is a bool, enforce boolean type
        if isinstance(default, bool):
            value = self._store.get(key, default)
            return bool(value)

        # Everything else: return stored or default
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value


def test_get_invalid_char_replacements(qtbot: QtBot) -> None:
    settings_dialog = SettingsDialog(FakeSettings())
    settings_dialog_gui = settings_dialog._ui
    qtbot.add_widget(settings_dialog_gui)
    settings_dialog_gui.invalid_char_table.set_data([("/", "⧸"), (":", "꞉")])
    assert settings_dialog.get_invalid_char_replacements() == [
        ("/", "⧸"),
        (":", "꞉"),
    ]
