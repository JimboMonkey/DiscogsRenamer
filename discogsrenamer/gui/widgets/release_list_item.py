from PyQt6 import QtWidgets

from discogsrenamer.gui.widgets.list_item_widget import ListItemWidget
from discogsrenamer.core.models.track_data import TrackData


class ReleaseListItem(QtWidgets.QListWidgetItem):
    def __init__(self, track_data: TrackData) -> None:
        super().__init__()
        self.track_data = track_data

    def create_widget(self) -> QtWidgets.QWidget:
        widget = ListItemWidget()
        widget.set_track_number(self.track_data.track_position)
        widget.set_original_filename(self.track_data.original_filename())
        self.setSizeHint(widget.sizeHint())
        return widget
