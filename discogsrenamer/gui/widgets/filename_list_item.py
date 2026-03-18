from PyQt6 import QtWidgets

from discogsrenamer.gui.widgets.list_item_widget import ListItemWidget


class FilenameListItem(QtWidgets.QListWidgetItem):
    def __init__(self, original_filename: str, new_filename: str = "") -> None:
        super().__init__()
        self.original_filename = original_filename
        self.new_filename = new_filename

    def create_widget(self) -> QtWidgets.QWidget:
        widget = ListItemWidget()
        widget.set_original_filename(self.original_filename)
        self.setSizeHint(widget.sizeHint())
        return widget
