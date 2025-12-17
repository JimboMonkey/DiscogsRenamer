from PyQt6 import QtWidgets, QtCore

from typing import Optional, Sequence
from collections import deque
from pathlib import Path

from gui.list_item_widget import ListItemWidget
from track_data import TrackData


class Tracklist(QtWidgets.QListWidget):

    tick_count = QtCore.pyqtSignal(int)
    all_ticked_new_filenames_filled = QtCore.pyqtSignal(bool)

    def __init__(
        self, editable: bool, parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        self._editable = editable
        super().__init__(parent)

        # Only folder list items should be selectable and draggable
        if self._editable:
            self.setDragDropMode(QtWidgets.QListWidget.DragDropMode.InternalMove)
        else:
            self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
            self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.model().rowsMoved.connect(self._number_and_shade)

    def populate(self, item_list: Sequence[QtWidgets.QListWidgetItem]) -> None:
        # Clear any existing items from the list
        self.clear()

        # For each track name in the list...
        for item in item_list:

            # Create and configure the custom widget
            widget = item.create_widget()

            self.addItem(item)
            self.setItemWidget(item, widget)
            widget._new_filename.setVisible(self._editable)
            widget._checkbox.stateChanged.connect(self.count_ticks)
            widget._checkbox.stateChanged.connect(
                self.check_all_ticked_new_filenames_filled
            )
            widget._new_filename.textChanged.connect(
                self.check_all_ticked_new_filenames_filled
            )

        # Update the track numbers and shading
        self._number_and_shade()
        self.count_ticks()

    def _number_and_shade(self):
        number_of_tracks = self.count()
        zfill_width = len(str(number_of_tracks))
        for index in range(number_of_tracks):
            tracklist_item = self.itemWidget(self.item(index))

            tracklist_item.set_track_number(str(index + 1).zfill(zfill_width))

            if index % 2 == 1:
                shaded = True
            else:
                shaded = False
            tracklist_item.set_shaded(shaded)

    def list_ticked_tracks(self) -> deque[TrackData] | None:

        ticked_tracks: deque[TrackData] = deque()

        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, ListItemWidget):
                if tracklist_item.is_ticked():
                    ticked_tracks.append(self.item(index).track_data)

        return ticked_tracks

    def list_track_renaming_info(self) -> list[tuple[str, Path, Path]] | None:
        ticked_tracks: list[tuple[str, Path, Path]] = []

        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, ListItemWidget):
                if tracklist_item.is_ticked():
                    ticked_tracks.append(
                        (
                            tracklist_item.get_track_number(),
                            Path(tracklist_item.get_original_filename()),
                            Path(tracklist_item.get_new_filename()),
                        )
                    )
        return ticked_tracks if ticked_tracks else None

    def apply_track_names(self, release_tracklist: deque[str] | None) -> None:
        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, ListItemWidget):
                if not release_tracklist:
                    break
                # Clear the lineedit first
                tracklist_item.set_new_filename("")
                if tracklist_item.is_ticked():
                    tracklist_item.set_new_filename(release_tracklist.popleft())

    def count_ticks(self) -> None:
        tick_count = 0
        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, ListItemWidget):
                if tracklist_item.is_ticked():
                    tick_count = tick_count + 1
        self.tick_count.emit(tick_count)

    def check_all_ticked_new_filenames_filled(self) -> None:
        tracklist_items = [
            self.itemWidget(self.item(index)) for index in range(self.count())
        ]

        all_ticked_new_filenames_filled = any(
            tracklist_item.is_ticked() for tracklist_item in tracklist_items
        ) and all(
            tracklist_item.new_filename_filled()
            for tracklist_item in tracklist_items
            if tracklist_item.is_ticked()
        )

        self.all_ticked_new_filenames_filled.emit(all_ticked_new_filenames_filled)
