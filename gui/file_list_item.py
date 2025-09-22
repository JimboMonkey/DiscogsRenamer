from PyQt6 import QtWidgets, QtCore

from typing import Optional


class FileListItem(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super(FileListItem, self).__init__(parent)

        # Allow the widgets background colour to be changed
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        # Create the display widgets
        self._track_number = QtWidgets.QLabel()
        self._original_filename = QtWidgets.QLabel()
        self._new_filename = QtWidgets.QLineEdit()

        # Set some spacing left and right of the track number
        self._track_number.setContentsMargins(15, 0, 15, 0)

        # Layout the filenames vertically
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self._original_filename)
        vertical_layout.addWidget(self._new_filename)

        # Layout the track number and filenames horizontally
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self._track_number)
        horizontal_layout.addLayout(vertical_layout)

        self.setLayout(horizontal_layout)

    # Set the track number label
    def set_track_number(self, text: str) -> None:
        self._track_number.setText(text)

    # Set the upper label with the original filename of the file
    def set_original_filename(self, text: str) -> None:
        self._original_filename.setText(text)

    # Set the lower lineedit with the new filename for the file
    def set_new_filename(self, text: str) -> None:
        self._new_filename.setText(text)

    # Shade the background of the widget
    # to make differentiation easier
    def set_shaded(self, shaded: bool) -> None:
        if shaded:
            self.setStyleSheet(
                """
                background-color: lightgray;
            """
            )
        else:
            self.setStyleSheet(
                """
                background-color: none;
            """
            )
