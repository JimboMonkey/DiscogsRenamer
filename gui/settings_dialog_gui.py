from PyQt6 import QtWidgets

from gui.invalid_char_tableview import InvalidCharTableView


class SettingsDialogGui(QtWidgets.QDialog):

    def __init__(self) -> None:
        super(QtWidgets.QDialog, self).__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Settings")

        format_label = QtWidgets.QLabel("Filename format:")

        self.format_lineedit = QtWidgets.QLineEdit()
        self.format_lineedit.setPlaceholderText("%number - %artist - %title")
        self.format_lineedit.setMinimumWidth(400)

        invalid_character_replacement_label = QtWidgets.QLabel(
            "Invalid Filename Character Replacements:"
        )
        self.invalid_char_table = InvalidCharTableView()

        zero_fill_checkbox = QtWidgets.QCheckBox("Zero-fill track numbers")
        zero_fill_checkbox.setChecked(True)

        misnumbering_warning_checkbox = QtWidgets.QCheckBox(
            "Warn about track misnumbering"
        )
        misnumbering_warning_checkbox.setChecked(True)

        self.restore_defaults_button = QtWidgets.QPushButton("Restore Defaults")
        self.close_button = QtWidgets.QPushButton("Close")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.restore_defaults_button)
        button_layout.addWidget(self.close_button)

        format_layout = QtWidgets.QHBoxLayout()
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_lineedit)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(format_layout)
        vertical_layout.addWidget(zero_fill_checkbox)
        vertical_layout.addWidget(misnumbering_warning_checkbox)
        vertical_layout.addWidget(invalid_character_replacement_label)
        vertical_layout.addWidget(self.invalid_char_table)
        vertical_layout.addLayout(button_layout)

        self.setLayout(vertical_layout)

    # Close the dialog
    def close_dialog(self) -> None:
        self.close()
