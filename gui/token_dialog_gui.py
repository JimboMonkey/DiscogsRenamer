from PyQt6 import QtWidgets, QtCore, QtGui

from auth_data_class import AuthenticationResult


class TokenDialogGui(QtWidgets.QDialog):

    def __init__(self) -> None:
        super(QtWidgets.QDialog, self).__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Discogs API Token")

        # Only ASCII letters and numbers
        regex = QtCore.QRegularExpression("[A-Za-z0-9]+")
        validator = QtGui.QRegularExpressionValidator(regex, self)

        token_message = QtWidgets.QLabel()
        token_message.setTextFormat(QtCore.Qt.TextFormat.RichText)
        token_message.setOpenExternalLinks(True)
        token_message.setText(
            "This application requires an authentication token, linked to your Discogs account, to be able to fetch tracklisting data from the Discogs site<br>"
            '<br>Go to <a href="https://www.discogs.com/settings/developers">https://www.discogs.com/settings/developers</a>, click on the "Generate new token" button, paste the generated token below, and hit "Save"<br>'
        )
        self._token_label = QtWidgets.QLabel("Token")
        self.token_lineedit = QtWidgets.QLineEdit()
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setToolTip("Save the token")
        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.setToolTip("Close the window")
        self._response_label = QtWidgets.QLabel()

        # Initially disable the save button
        self.save_button.setEnabled(False)

        self.token_lineedit.setPlaceholderText("Enter your Discogs API token")
        self.token_lineedit.setMinimumWidth(350)
        self.token_lineedit.setValidator(validator)
        self.token_lineedit.textChanged.connect(self._save_button_enabled)

        green_tick_icon = QtGui.QIcon("gui/icons/green_tick.svg")
        red_cross_icon = QtGui.QIcon("gui/icons/red_cross.svg")
        icon_size = QtCore.QSize(16, 16)
        self._icon_label = QtWidgets.QLabel()
        self._icon_label.setFixedSize(icon_size)
        self.green_tick_pixmap = green_tick_icon.pixmap(icon_size)
        self.red_cross_pixmap = red_cross_icon.pixmap(icon_size)

        response_layout = QtWidgets.QHBoxLayout()
        response_layout.addWidget(self._icon_label)
        response_layout.addWidget(self._response_label)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self._token_label, 0, 0)
        layout.addWidget(self.token_lineedit, 0, 1)
        layout.addLayout(response_layout, 1, 1)
        layout.addWidget(self.save_button, 0, 2)
        layout.addWidget(self.close_button, 0, 3)

        self._vertical_layout = QtWidgets.QVBoxLayout()
        self._vertical_layout.addWidget(token_message)
        self._vertical_layout.addLayout(layout)

        self.setLayout(self._vertical_layout)

    # Enable the save button only if there is text in the line edit
    def _save_button_enabled(self) -> None:
        if self.token_lineedit.text():
            enabled = True
        else:
            enabled = False
        self.save_button.setEnabled(enabled)

    # Close the dialog
    def close_dialog(self) -> None:
        self.close()

    def set_authentication_state(self, result: AuthenticationResult) -> None:
        self._response_label.setText(result.message)
        if result.status:
            self._icon_label.setPixmap(self.green_tick_pixmap)
        else:
            self._icon_label.setPixmap(self.red_cross_pixmap)
