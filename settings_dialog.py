from settings_protocol import SettingsProtocol
from gui.settings_dialog_gui import SettingsDialogGui

from filename_rules import get_platform_invalid_characters


class SettingsDialog:

    def __init__(self, settings: SettingsProtocol) -> None:

        self._settings = settings
        self._ui = SettingsDialogGui()
        self._ui.invalid_char_table.set_data(
            self.load_invalid_char_replacements(settings)
        )

        self._init_connections()

    def show(self) -> None:
        self._ui.exec()  # only run modal loop when explicitly asked

    # Link GUI widgets to the functions
    def _init_connections(self) -> None:
        self._ui.close_button.clicked.connect(self._ui.close_dialog)
        self._ui.close_button.clicked.connect(self.save_settings)

    def set_filename_format(self) -> None:
        self._ui.format_lineedit.setText(self._settings.get("filename_format"))

    def get_filename_format(self) -> str:
        return self._ui.format_lineedit.text()

    def save_settings(self) -> None:
        self._settings.set("filename_format", self.get_filename_format())
