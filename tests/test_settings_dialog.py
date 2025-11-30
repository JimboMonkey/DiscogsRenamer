from pytestqt.qtbot import QtBot

from settings_dialog import SettingsDialog


def test_get_filename_format(qtbot: QtBot) -> None:
    settings_dialog = SettingsDialog()
    settings_dialog_gui = settings_dialog._ui
    qtbot.add_widget(settings_dialog_gui)

    test_string = "%a - %b - %c"
    settings_dialog_gui.format_lineedit.setText(test_string)

    assert settings_dialog.get_filename_format() == test_string

    settings_dialog_gui.close()
