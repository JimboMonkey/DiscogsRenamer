from PyQt6 import QtWidgets, QtGui, QtCore
from typing import Optional
from pathlib import Path

from gui.toolbar import Toolbar
from gui.tracklist import Tracklist

from constants import APP_NAME


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:

        self.ticked_release_tracks = 0
        self.ticked_folder_tracks = 0

        self.setWindowTitle(APP_NAME)

        self.toolbar = Toolbar()

        release_label = QtWidgets.QLabel("Release")
        folder_label = QtWidgets.QLabel("Folder")

        # Only allow release to be specified in form [r12345], r12345, or 12345
        regex = QtCore.QRegularExpression(r"(?:^\d+$|^\[r\d+\]$|^r\d+$)")
        validator = QtGui.QRegularExpressionValidator(regex, self)

        release_number_label = QtWidgets.QLabel("Discogs Release Number")
        self.load_release_button = QtWidgets.QPushButton("Load Release")
        self.load_release_button.setEnabled(False)
        self.release_lineedit = QtWidgets.QLineEdit()
        self.release_lineedit.setPlaceholderText(
            "Enter the Discogs release number you wish to load eg [r180865] or 180865"
        )
        self.release_lineedit.setValidator(validator)

        self.release_lineedit.textChanged.connect(self.load_release_button_enabled)

        self.release_artist_title_label = QtWidgets.QLabel()

        self.file_browser_button = QtWidgets.QPushButton("Browse")
        self.folder_entry_label = QtWidgets.QLabel()

        release_entry_layout = QtWidgets.QHBoxLayout()
        release_entry_layout.addWidget(release_number_label)
        release_entry_layout.addWidget(self.release_lineedit)
        release_entry_layout.addWidget(self.load_release_button)
        # Ensure the label expands horizontally
        self.folder_entry_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )

        self.transfer_button = QtWidgets.QPushButton(">>>>")
        self.transfer_button.setEnabled(False)

        self.apply_button = QtWidgets.QPushButton("Apply")
        self.apply_button.setEnabled(False)

        self.tick_count = QtWidgets.QLabel()
        self.tick_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        middle_layout = QtWidgets.QVBoxLayout()
        middle_layout.addStretch(1)
        middle_layout.addWidget(self.transfer_button)
        middle_layout.addWidget(self.tick_count)
        middle_layout.addStretch(1)

        folder_entry_layout = QtWidgets.QHBoxLayout()
        folder_entry_layout.addWidget(self.file_browser_button)
        folder_entry_layout.addWidget(self.folder_entry_label)

        self.release_listwidget = Tracklist(editable=False)
        self.folder_listwidget = Tracklist(editable=True)

        release_layout = QtWidgets.QVBoxLayout()
        release_layout.addWidget(release_label)
        release_layout.addLayout(release_entry_layout)
        release_layout.addWidget(self.release_artist_title_label)
        release_layout.addWidget(self.release_listwidget)

        folder_layout = QtWidgets.QVBoxLayout()
        folder_layout.addWidget(folder_label)
        folder_layout.addLayout(folder_entry_layout)
        folder_layout.addWidget(self.folder_listwidget)

        listwidget_layout = QtWidgets.QHBoxLayout()
        listwidget_layout.addLayout(release_layout)
        listwidget_layout.addLayout(middle_layout)
        listwidget_layout.addLayout(folder_layout)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.toolbar)
        vertical_layout.addLayout(listwidget_layout)
        vertical_layout.addWidget(
            self.apply_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight
        )

        # Set the listwidget layout as the layout for the window
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)

        self.showMaximized()

    # Enable the load release button only if
    # there is valid text in the line edit
    def load_release_button_enabled(self) -> None:
        if self.release_lineedit.text() and self.release_lineedit.hasAcceptableInput():
            enabled = True
        else:
            enabled = False
        self.load_release_button.setEnabled(enabled)

    def apply_button_enabled(self, enabled: bool) -> None:
        self.apply_button.setEnabled(enabled)

    def handle_tick_count(self, tick_count: int, release_tracklist: bool) -> None:
        if release_tracklist:
            self.ticked_release_tracks = tick_count
        else:
            self.ticked_folder_tracks = tick_count

        self.update_tick_count_label()
        self.compare_counts()

    def update_tick_count_label(self):
        self.tick_count.setText(
            f"{self.ticked_release_tracks} vs {self.ticked_folder_tracks} \n selected"
        )

    def compare_counts(self):
        if self.ticked_release_tracks == self.ticked_folder_tracks and (
            self.ticked_release_tracks != 0 or self.ticked_folder_tracks != 0
        ):
            self.transfer_button.setEnabled(True)
        else:
            self.transfer_button.setEnabled(False)

    def update_release_artist_title_label(self, artist: str, title: str) -> None:
        self.release_artist_title_label.setText(f"{artist} - {title}")

    def set_folder_path_label(self, folder_path: str) -> None:
        self.folder_entry_label.setText(folder_path)

    def get_folder_path(self) -> Path | None:
        folder_path = self.folder_entry_label.text()
        return Path(folder_path) if folder_path.strip() else None
