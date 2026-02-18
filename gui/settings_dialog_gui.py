from PyQt6 import QtWidgets

from gui.invalid_char_tableview import InvalidCharTableView
from filename_rules import MAX_FILENAME_LENGTH
from app_settings import DEFAULT_SETTINGS


class SettingsDialogGui(QtWidgets.QDialog):

    def __init__(self) -> None:
        super(QtWidgets.QDialog, self).__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Settings")

        format_label = QtWidgets.QLabel("Filename format:")

        self.format_lineedit = QtWidgets.QLineEdit()
        self.format_lineedit.setMaxLength(MAX_FILENAME_LENGTH)
        self.format_lineedit.setPlaceholderText(DEFAULT_SETTINGS["filename_format"])
        self.format_lineedit.setMinimumWidth(400)

        invalid_character_replacement_label = QtWidgets.QLabel(
            "Invalid Filename Character Replacements:"
        )
        self.invalid_char_table = InvalidCharTableView()

        self.zero_fill_checkbox = QtWidgets.QCheckBox("Zero-fill folder track numbers")
        self.zero_fill_checkbox.setChecked(True)

        misnumbering_warning_checkbox = QtWidgets.QCheckBox(
            "Warn about track misnumbering"
        )
        misnumbering_warning_checkbox.setChecked(True)

        self.restore_defaults_button = QtWidgets.QPushButton("Restore Defaults")
        self.restore_defaults_button.setToolTip("Restore default settings")
        self.close_button = QtWidgets.QPushButton("Save && Close")
        self.close_button.setToolTip("Save the settings and close the window")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.restore_defaults_button)
        button_layout.addWidget(self.close_button)

        format_layout = QtWidgets.QHBoxLayout()
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_lineedit)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(format_layout)
        vertical_layout.addWidget(self.zero_fill_checkbox)
        vertical_layout.addWidget(misnumbering_warning_checkbox)
        vertical_layout.addWidget(invalid_character_replacement_label)
        vertical_layout.addWidget(self.invalid_char_table)
        vertical_layout.addLayout(button_layout)

        self.setLayout(vertical_layout)

    # Close the dialog
    def close_dialog(self) -> None:
        self.close()
