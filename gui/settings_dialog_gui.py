from PyQt6 import QtWidgets


class SettingsDialogGui(QtWidgets.QDialog):

    def __init__(self) -> None:
        super(QtWidgets.QDialog, self).__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Settings")

        format_label = QtWidgets.QLabel("Filename format:")

        self.format_lineedit = QtWidgets.QLineEdit()
        self.format_lineedit.setPlaceholderText("%number - %artist - %title")
        self.format_lineedit.setMinimumWidth(200)

        slash_replacement_label = QtWidgets.QLabel(
            "Character to replace slashes (/ or \\)"
        )

        slash_replacement_linedit = QtWidgets.QLineEdit()
        slash_replacement_linedit.setPlaceholderText(",")
        slash_replacement_linedit.setMinimumWidth(200)

        zero_fill_checkbox = QtWidgets.QCheckBox("Zero-fill track numbers")
        zero_fill_checkbox.setChecked(True)

        misnumbering_warning_checkbox = QtWidgets.QCheckBox(
            "Warn about track misnumbering"
        )
        misnumbering_warning_checkbox.setChecked(True)

        self.close_button = QtWidgets.QPushButton("Close")

        format_layout = QtWidgets.QHBoxLayout()
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_lineedit)

        slash_replacement_layout = QtWidgets.QHBoxLayout()
        slash_replacement_layout.addWidget(slash_replacement_label)
        slash_replacement_layout.addWidget(slash_replacement_linedit)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(format_layout)
        vertical_layout.addLayout(slash_replacement_layout)
        vertical_layout.addWidget(zero_fill_checkbox)
        vertical_layout.addWidget(misnumbering_warning_checkbox)
        vertical_layout.addWidget(self.close_button)

        self.setLayout(vertical_layout)

    # Close the dialog
    def close_dialog(self) -> None:
        self.close()
