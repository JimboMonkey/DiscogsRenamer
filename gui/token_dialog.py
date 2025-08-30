from PyQt6 import QtWidgets, QtCore, QtGui


class TokenDialogGui(QtWidgets.QDialog):

    def __init__(self) -> None:
        super(QtWidgets.QDialog, self).__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Discogs API Token")

        # Only ASCII letters and numbers
        regex = QtCore.QRegularExpression("[A-Za-z0-9]+")
        validator = QtGui.QRegularExpressionValidator(regex, self)

        self._token_label = QtWidgets.QLabel("Token")
        self._token_lineedit = QtWidgets.QLineEdit(self)
        self._token_lineedit.setPlaceholderText("Enter your Discogs API token")
        self._token_lineedit.setMinimumWidth(350)
        self._token_lineedit.setValidator(validator)

        self._token_lineedit.textChanged.connect(self._save_button_enabled)

        self._save_button = QtWidgets.QPushButton("Save")
        self._close_button = QtWidgets.QPushButton("Close")

        self._save_button.setEnabled(False)
        # self._save_button.clicked.connect(self._save_token)
        self._close_button.clicked.connect(self._close_dialog)

        self._horizontal_layout = QtWidgets.QHBoxLayout(self)
        self._horizontal_layout.addWidget(self._token_label)
        self._horizontal_layout.addWidget(self._token_lineedit)
        self._horizontal_layout.addWidget(self._save_button)
        self._horizontal_layout.addWidget(self._close_button)

        self.setLayout(self._horizontal_layout)

    # Enable the save button only if there is text in the line edit
    def _save_button_enabled(self) -> None:
        if self._token_lineedit.text():
            enabled = True
        else:
            enabled = False
        self._save_button.setEnabled(enabled)

    # Close the dialog
    def _close_dialog(self) -> None:
        self.close()
