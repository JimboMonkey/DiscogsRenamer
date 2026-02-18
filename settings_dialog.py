from settings_protocol import SettingsProtocol
from gui.settings_dialog_gui import SettingsDialogGui

from filename_rules import get_invalid_filename_characters
from gui.utils import make_filename_validator
from app_settings import DEFAULT_SETTINGS


class SettingsDialog:

    def __init__(self, settings: SettingsProtocol) -> None:

        self._settings = settings
        self._ui = SettingsDialogGui()
        self._ui.format_lineedit.setText(self.load_filename_format(settings))
        self._ui.format_lineedit.setValidator(make_filename_validator())
        self._ui.invalid_char_table.set_data(
            self.load_invalid_char_replacements(settings)
        )

        self._init_connections()

    def show(self) -> None:
        self._ui.exec()  # only run modal loop when explicitly asked

    # Link GUI widgets to the functions
    def _init_connections(self) -> None:
        self._ui.cancel_button.clicked.connect(self._ui.close_dialog)
        self._ui.restore_defaults_button.clicked.connect(self.restore_defaults)
        self._ui.close_button.clicked.connect(self._ui.close_dialog)
        self._ui.close_button.clicked.connect(self.save_settings)
        self._ui.close_button.clicked.connect(self.get_invalid_char_replacements)

    def set_filename_format(self) -> None:
        self._ui.format_lineedit.setText(self._settings.get("filename_format"))

    def get_filename_format(self) -> str:
        return self._ui.format_lineedit.text()

    def get_invalid_char_replacements(self) -> list[tuple[str, str]]:
        return self._ui.invalid_char_table.model().get_data()

    def save_settings(self) -> None:
        self._settings.set("filename_format", self.get_filename_format())
        self._settings.set("zero_fill_enabled", self._ui.zero_fill_checkbox.isChecked())
        self._settings.set(
            "invalid_char_replacements", self.get_invalid_char_replacements()
        )

    def restore_defaults(self):
        self._ui.format_lineedit.setText(DEFAULT_SETTINGS["filename_format"])
        self._ui.zero_fill_checkbox.setChecked(DEFAULT_SETTINGS["zero_fill_enabled"])
        self._ui.invalid_char_table.set_data(
            DEFAULT_SETTINGS["invalid_char_replacements"]
        )

    def load_filename_format(self, store: SettingsProtocol) -> str:
        raw = store.get("filename_format")

        # No entry → use defaults
        if raw is None:
            return "%num - %track_title"
        return raw

    def load_invalid_char_replacements(
        self, store: SettingsProtocol
    ) -> list[tuple[str, str]]:
        raw = store.get("invalid_char_replacements")

        # No entry → use defaults
        if raw is None:
            return get_invalid_filename_characters()

        return raw
