from PyQt6 import QtWidgets
from pathlib import Path

from discogsrenamer.gui.widgets.invalid_char_tableview import InvalidCharTableView
from discogsrenamer.core.filename_rules import MAX_FILENAME_LENGTH
from discogsrenamer.core.app_settings import DEFAULT_SETTINGS
from discogsrenamer.gui.utils import open_folder_dialog


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

        format_specifier_list_label = QtWidgets.QLabel(
            "<table>"
            "<tr><td style='padding-right: 20px;'><strong>%ra</strong></td><td>Release artist</td></tr>"
            "<tr><td style='padding-right: 20px;'><strong>%rt</strong></td><td>Release title</td></tr>"
            "<tr><td style='padding-right: 20px;'><strong>%rn</strong></td><td>Release track number</td></tr>"
            "<tr><td style='padding-right: 20px;'><strong>%ta</strong></td><td>Track artist</td></tr>"
            "<tr><td style='padding-right: 20px;'><strong>%tt</strong></td><td>Track title</td></tr>"
            "<tr><td style='padding-right: 20px;'><strong>%fn</strong></td><td>Folder track number</td></tr>"
            "</table>"
        )

        invalid_character_replacement_label = QtWidgets.QLabel(
            "Invalid Filename Character Replacements:"
        )
        self.invalid_char_table = InvalidCharTableView()

        self.zero_fill_checkbox = QtWidgets.QCheckBox("Zero-fill folder track numbers")
        self.zero_fill_checkbox.setChecked(True)

        self.misnumbering_warning_checkbox = QtWidgets.QCheckBox(
            "Highlight track misnumbering"
        )
        self.misnumbering_warning_checkbox.setChecked(True)

        initial_folder_label = QtWidgets.QLabel("Initial folder path")
        self.initial_folder_lineedit = QtWidgets.QLineEdit()
        self.initial_folder_lineedit.setText(str(DEFAULT_SETTINGS["initial_folder"]))
        self.initial_folder_lineedit.setReadOnly(True)
        self.initial_folder_button = QtWidgets.QPushButton("Select")

        initial_folder_layout = QtWidgets.QHBoxLayout()
        initial_folder_layout.addWidget(initial_folder_label)
        initial_folder_layout.addWidget(self.initial_folder_lineedit)
        initial_folder_layout.addWidget(self.initial_folder_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setToolTip("Close the window")
        self.restore_defaults_button = QtWidgets.QPushButton("Restore Defaults")
        self.restore_defaults_button.setToolTip("Restore default settings")
        self.close_button = QtWidgets.QPushButton("Save && Close")
        self.close_button.setToolTip("Save the settings and close the window")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.restore_defaults_button)
        button_layout.addWidget(self.close_button)

        filename_format_layout = QtWidgets.QGridLayout()
        filename_format_layout.addWidget(format_label, 0, 0)
        filename_format_layout.addWidget(self.format_lineedit, 0, 1)
        filename_format_layout.addWidget(format_specifier_list_label, 1, 1)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(filename_format_layout)
        vertical_layout.addWidget(self.zero_fill_checkbox)
        vertical_layout.addWidget(self.misnumbering_warning_checkbox)
        vertical_layout.addLayout(initial_folder_layout)
        vertical_layout.addWidget(invalid_character_replacement_label)
        vertical_layout.addWidget(self.invalid_char_table)
        vertical_layout.addLayout(button_layout)

        self.setLayout(vertical_layout)

    def open_initial_folder_dialog(self) -> None:
        folder_path = open_folder_dialog(self, self.initial_folder_lineedit.text())

        # Check for file validity here so that cancelling
        # the open dialog doesn't set a blank path
        if (folder_path) and (Path(folder_path).exists()):
            self.initial_folder_lineedit.setText(str(Path(folder_path)))

    # Close the dialog
    def close_dialog(self) -> None:
        self.close()
