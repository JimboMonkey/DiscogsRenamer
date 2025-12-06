from PyQt6 import QtWidgets

from gui.list_item_widget import ListItemWidget


class ReleaseListItem(QtWidgets.QListWidgetItem):
    def __init__(self, track_artists: str, track_title: str) -> None:
        super().__init__()
        self.track_artists = track_artists
        self.track_title = track_title

    def create_widget(self) -> QtWidgets.QWidget:
        widget = ListItemWidget()
        if self.track_artists:
            widget.set_original_filename(f"{self.track_artists} - {self.track_title}")
        else:
            widget.set_original_filename(f"{self.track_title}")
        self.setSizeHint(widget.sizeHint())
        return widget
