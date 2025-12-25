from PyQt6 import QtWidgets, QtCore

from typing import Optional
from filename_rules import get_platform_invalid_characters
from invalid_char_model import InvalidCharModel


class InvalidCharTableView(QtWidgets.QTableView):

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # Construct a model from the invalid characters
        # of the current platform (Windows or Unix)
        platform_invalid_chars = get_platform_invalid_characters()
        model = InvalidCharModel(platform_invalid_chars)
        self.setModel(model)

        # Setup the UI
        self._init_ui()

        # Resize to the number of rows
        # The inclusion of the frame width avoids
        # scroll bars to accommodate the frame
        rows_height = sum(self.rowHeight(row) for row in range(self.model().rowCount()))
        total_height = (
            rows_height + self.horizontalHeader().height() + 2 * self.frameWidth()
        )
        self.setMinimumHeight(total_height)
        self.setMaximumHeight(total_height)

    def _init_ui(self) -> None:

        # Fill the available space horizontally
        # and don't show a vertical header
        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.verticalHeader().setVisible(False)

        # Allow the second column to be editable with a
        # single click without highlighting on selection
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
