from PyQt6 import QtWidgets, QtGui, QtCore
from typing import Optional
from pathlib import Path

from gui.toolbar import Toolbar
from gui.tracklist_item import TracklistItem

from constants import APP_NAME


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(APP_NAME)

        self.toolbar = Toolbar()

        release_label = QtWidgets.QLabel("Release")
        folder_label = QtWidgets.QLabel("Folder")

        # Only allow release to be specified in form [r12345], r12345, or 12345
        regex = QtCore.QRegularExpression(r"(?:^\d+$|^\[r\d+\]$|^r\d+$)")
        validator = QtGui.QRegularExpressionValidator(regex, self)

        release_number_label = QtWidgets.QLabel("Discogs Release Number")
        self._load_release_button = QtWidgets.QPushButton("Load Release")
        self._load_release_button.setEnabled(False)
        self._release_lineedit = QtWidgets.QLineEdit()
        self._release_lineedit.setPlaceholderText(
            "Enter the Discogs release number you wish to load eg [r180865] or 180865"
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
        self._folder_listwidget = QtWidgets.QListWidget()
        self._folder_listwidget.setDragDropMode(
            QtWidgets.QListWidget.DragDropMode.InternalMove
        )
        self._folder_listwidget.model().rowsMoved.connect(self.on_rows_moved)

        release_layout = QtWidgets.QVBoxLayout()
        release_layout.addWidget(release_label)
        release_layout.addLayout(release_entry_layout)
        release_layout.addWidget(release_listwidget)

        folder_layout = QtWidgets.QVBoxLayout()
        folder_layout.addWidget(folder_label)
        folder_layout.addLayout(folder_entry_layout)
        folder_layout.addWidget(self._folder_listwidget)

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

    # Populate the folder list with the given list of file paths
    def populate_folder_list(self, file_list: list[Path]) -> None:
        # Clear any existing items from the list
        self._folder_listwidget.clear()

        # For each file path in the list...
        for file_path in file_list:

            # Create and configure the custom widget
            file_list_item = TracklistItem()
            file_list_item.set_original_filename(file_path.name)

            # Create a QListWidgetItem and add it to the list
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setSizeHint(file_list_item.sizeHint())
            self._folder_listwidget.addItem(list_widget_item)

            # Embed the custom widget into the item
            self._folder_listwidget.setItemWidget(list_widget_item, file_list_item)

        # Update the track numbers and shading
        self.on_rows_moved()

    def on_rows_moved(self):
        for index in range(self._folder_listwidget.count()):
            item = self._folder_listwidget.item(index)
            widget: FileListItem = self._folder_listwidget.itemWidget(item)

            widget.set_track_number(str(index + 1))

            if index % 2 == 1:
                shaded = True
            else:
                shaded = False
            widget.set_shaded(shaded)
