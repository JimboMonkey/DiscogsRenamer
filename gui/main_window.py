from PyQt6 import QtWidgets
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

        web_browser_button = QtWidgets.QPushButton("Browse")
        release_text_entry = QtWidgets.QLineEdit()

        file_browser_button = QtWidgets.QPushButton("Browse")
        folder_entry_label = QtWidgets.QLabel()

        release_entry_layout = QtWidgets.QHBoxLayout()
        release_entry_layout.addWidget(web_browser_button)
        release_entry_layout.addWidget(release_text_entry)

        folder_entry_layout = QtWidgets.QHBoxLayout()
        folder_entry_layout.addWidget(file_browser_button)
        folder_entry_layout.addWidget(folder_entry_label)

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

    def open_token_dialog(self) -> None:
        dialog = TokenDialogGui()
        dialog.exec()
