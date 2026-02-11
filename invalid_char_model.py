from PyQt6 import QtCore, QtWidgets

from typing import Any


class InvalidCharModel(QtCore.QAbstractTableModel):
    def __init__(
        self,
        invalid_chars: list[tuple[str, str]],
        parent_widget: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__()
        self.parent_widget = parent_widget
        self._rows = [
            {"character": char, "replacement": default}
            for char, default in invalid_chars
        ]

    # Optional implementation of abstract method
    # Returns the header labels
    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            role == QtCore.Qt.ItemDataRole.DisplayRole
            and orientation == QtCore.Qt.Orientation.Horizontal
        ):
            if section == 0:
                return "Invalid Character"
            if section == 1:
                return "Replacement"
        return None

    # Required implementation of abstract method
    # Returns the number of rows in the dataset
    def rowCount(self, parent: QtCore.QModelIndex | None = None) -> int:
        return len(self._rows)

    # Required implementation of abstract method
    # Returns the number of columns in each row
    def columnCount(self, parent: QtCore.QModelIndex | None = None) -> int:
        return 2  # character, replacement

    # Required implementation of abstract method
    # Handles how data is displayed in the table
    def data(
        self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole
    ) -> Any:
        if not index.isValid():
            return None

        row = self._rows[index.row()]
        col = index.column()

        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return row["character"]
            if col == 1:
                return row["replacement"]

        if role == QtCore.Qt.ItemDataRole.EditRole and col == 1:
            return row["replacement"]

        return None

    # Allow the 'replacement' column
    # of the model to be editable
    def setData(
        self,
        index: QtCore.QModelIndex,
        value: str,
        role: int = QtCore.Qt.ItemDataRole.EditRole,
    ) -> bool:
        if role == QtCore.Qt.ItemDataRole.EditRole and index.column() == 1:

            # Build a list of the invalid characters listed in first column
            invalid_chars = {row["character"] for row in self._rows}

            # Reject replacement characters which appear in
            # the first column or which are more than one character long
            if value in invalid_chars:
                QtWidgets.QMessageBox.warning(
                    self.parent_widget,
                    "Invalid Replacement Character",
                    "Replacement character cannot be an invalid character",
                )
                return False

            # Reject replacement characters which are more than one character long
            if len(value) > 1:
                QtWidgets.QMessageBox.warning(
                    self.parent_widget,
                    "Invalid Replacement Character",
                    "Replacement character must be a single character or blank",
                )
                return False

            self._rows[index.row()]["replacement"] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    # Allow only the second column to be edtable
    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() == 1:
            return (
                QtCore.Qt.ItemFlag.ItemIsSelectable
                | QtCore.Qt.ItemFlag.ItemIsEnabled
                | QtCore.Qt.ItemFlag.ItemIsEditable
            )
        return QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled

    def get_data(self) -> list[tuple[str, str]]:
        return [(row["character"], row["replacement"]) for row in self._rows]
