from pytestqt.qtbot import QtBot
from typing import Any

from settings_dialog import SettingsDialog


def test_get_filename_format(qtbot: QtBot) -> None:
    settings_dialog = SettingsDialog(FakeSettings())
    settings_dialog_gui = settings_dialog._ui
    qtbot.add_widget(settings_dialog_gui)

    test_string = "%a - %b - %c"
    settings_dialog_gui.format_lineedit.setText(test_string)

    assert settings_dialog.get_filename_format() == test_string

    settings_dialog_gui.close()


class FakeSettings:
    def __init__(self):
        self.store = {}

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value: Any):
        self.store[key] = value


def test_get_invalid_char_replacements(qtbot: QtBot) -> None:
    settings_dialog = SettingsDialog(FakeSettings())
    settings_dialog_gui = settings_dialog._ui
    qtbot.add_widget(settings_dialog_gui)
    settings_dialog_gui.invalid_char_table.set_data([("/", "⧸"), (":", "꞉")])
    assert settings_dialog.get_invalid_char_replacements() == [
        ("/", "⧸"),
        (":", "꞉"),
    ]
