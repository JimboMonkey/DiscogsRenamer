from PyQt6 import QtWidgets

from typing import Optional

from gui.tracklist_item import TracklistItem


class Tracklist(QtWidgets.QListWidget):
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

            # Create a QListWidgetItem and add it to the list
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setSizeHint(tracklist_item.sizeHint())
            tracklist_item._new_filename.setVisible(self._editable)

            self.addItem(list_widget_item)

            # Embed the custom widget into the item
            self.setItemWidget(list_widget_item, tracklist_item)

        # Update the track numbers and shading
        self._number_and_shade()

    def _number_and_shade(self):
        number_of_tracks = self.count()
        zfill_width = len(str(number_of_tracks))
        for index in range(number_of_tracks):
            item = self.item(index)
            tracklist_item: TracklistItem = self.itemWidget(item)

            tracklist_item.set_track_number(str(index + 1).zfill(zfill_width))

            if index % 2 == 1:
                shaded = True
            else:
                shaded = False
            tracklist_item.set_shaded(shaded)
