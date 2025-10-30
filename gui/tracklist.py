from PyQt6 import QtWidgets, QtCore

from typing import Optional
from collections import deque

from gui.tracklist_item import TracklistItem


class Tracklist(QtWidgets.QListWidget):

    tick_count = QtCore.pyqtSignal(int)

    def __init__(
        self, editable: bool, parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        self._editable = editable
        super().__init__(parent)

        if self._editable:
            self.setDragDropMode(QtWidgets.QListWidget.DragDropMode.InternalMove)

        self.model().rowsMoved.connect(self._number_and_shade)

    def populate(self, track_list: list[str]) -> None:
        # Clear any existing items from the list
        self.clear()

        # For each track name in the list...
        for track in track_list:

            # Create and configure the custom widget
            tracklist_item = TracklistItem()
            tracklist_item.set_original_filename(track)
            tracklist_item._checkbox.stateChanged.connect(self.count_ticks)

            # Create a QListWidgetItem and add it to the list
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setSizeHint(tracklist_item.sizeHint())
            tracklist_item._new_filename.setVisible(self._editable)

            self.addItem(list_widget_item)

            # Embed the custom widget into the item
            self.setItemWidget(list_widget_item, tracklist_item)

        # Update the track numbers and shading
        self._number_and_shade()
        self.count_ticks()

    def _number_and_shade(self):
        number_of_tracks = self.count()
        zfill_width = len(str(number_of_tracks))
        for index in range(number_of_tracks):
            item = self.item(index)
            tracklist_item: TracklistItem = self.itemWidget(item)

            tracklist_item.set_track_number(str(index + 1).zfill(zfill_width))

    def list_ticked_tracks(self) -> deque[str] | None:

        ticked_tracks: deque[str] = deque()

        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, TracklistItem):
                if tracklist_item.is_ticked():
                    ticked_tracks.append(tracklist_item.get_original_filename())

        return ticked_tracks

    def apply_track_names(self, release_tracklist: deque[str] | None) -> None:
        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, TracklistItem):
                if not release_tracklist:
                    break
                if tracklist_item.is_ticked():
                    tracklist_item.set_new_filename(release_tracklist.popleft())

    def count_ticks(self) -> None:
        tick_count = 0
        for index in range(self.count()):
            tracklist_item = self.itemWidget(self.item(index))
            if isinstance(tracklist_item, TracklistItem):
                if tracklist_item.is_ticked():
                    tick_count = tick_count + 1
        self.tick_count.emit(tick_count)
