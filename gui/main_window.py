from PyQt6 import QtWidgets, QtGui, QtCore
from typing import Optional

from gui.token_dialog import TokenDialogGui

from constants import APP_NAME


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(APP_NAME)

        release_label = QtWidgets.QLabel("Release")
        folder_label = QtWidgets.QLabel("Folder")

        # Only allow release to be specified in form r[12345], r12345, or 12345
        regex = QtCore.QRegularExpression(r"(?:^\d+$|^r\[\d+\]$|^r\d+$)")
        validator = QtGui.QRegularExpressionValidator(regex, self)

        release_number_label = QtWidgets.QLabel("Discogs Release Number")
        self._load_release_button = QtWidgets.QPushButton("Load Release")
        self._load_release_button.setEnabled(False)
        self._release_lineedit = QtWidgets.QLineEdit()
        self._release_lineedit.setPlaceholderText(
            "Enter the Discogs release number you wish to load eg r[180865] or 180865"
        )
        self._release_lineedit.setValidator(validator)

        self._release_lineedit.textChanged.connect(self.load_release_button_enabled)

        self.file_browser_button = QtWidgets.QPushButton("Browse")
        self.folder_entry_label = QtWidgets.QLabel()

        release_entry_layout = QtWidgets.QHBoxLayout()
        release_entry_layout.addWidget(release_number_label)
        release_entry_layout.addWidget(self._release_lineedit)
        release_entry_layout.addWidget(self._load_release_button)
        # Ensure the label expands horizontally
        self.folder_entry_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )

        folder_entry_layout = QtWidgets.QHBoxLayout()
        folder_entry_layout.addWidget(self.file_browser_button)
        folder_entry_layout.addWidget(self.folder_entry_label)

        release_listwidget = QtWidgets.QListWidget()
        folder_listwidget = QtWidgets.QListWidget()

        release_layout = QtWidgets.QVBoxLayout()
        release_layout.addWidget(release_label)
        release_layout.addLayout(release_entry_layout)
        release_layout.addWidget(release_listwidget)

        folder_layout = QtWidgets.QVBoxLayout()
        folder_layout.addWidget(folder_label)
        folder_layout.addLayout(folder_entry_layout)
        folder_layout.addWidget(folder_listwidget)

        listwidget_layout = QtWidgets.QHBoxLayout()
        listwidget_layout.addLayout(release_layout)
        listwidget_layout.addLayout(folder_layout)

        # Set the listwidget layout as the layout for the window
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(listwidget_layout)
        self.setCentralWidget(central_widget)

        # self.open_token_dialog()
        self.show()

    # Enable the load release button only if
    # there is valid text in the line edit
    def load_release_button_enabled(self) -> None:
        if (
            self._release_lineedit.text()
            and self._release_lineedit.hasAcceptableInput()
        ):
            enabled = True
        else:
            enabled = False
        self._load_release_button.setEnabled(enabled)

    def open_token_dialog(self) -> None:
        dialog = TokenDialogGui()
        dialog.exec()
