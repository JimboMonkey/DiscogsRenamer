from PyQt6 import QtCore, QtWidgets

from gui.main_window import MainWindow

from pathlib import Path
from os.path import expanduser


class MainManager(QtCore.QObject):

    def __init__(self) -> None:
        # Create the main GUI window
        self._ui = MainWindow()

        self._ui.file_browser_button.pressed.connect(self._show_open_dialog)
        super(MainManager, self).__init__()

    # Return a QFileDialog for 'Open'
    def _open_dialog(self) -> str:
        return QtWidgets.QFileDialog.getExistingDirectory(
            self._ui,
            "Select Folder",
            expanduser("."),
            options=QtWidgets.QFileDialog.Option.ShowDirsOnly
            | QtWidgets.QFileDialog.Option.DontUseNativeDialog,
        )

    # Use the standard open dialog box to get the file path of a folder
    def _show_open_dialog(self) -> None:
        file_path = self._open_dialog()

        # Check for file validity here so that cancelling
        # the open dialog doesn't set a blank path
        if (file_path) and (Path(file_path).exists()):
            self._open_file(Path(file_path))

    # Set a file path in the GUI, config file, and database
    # Then trigger a load of its categories
    def _open_file(self, file_path: Path) -> None:
        self._ui.folder_entry_label.setText(str(file_path))
        self._list_files_in_folder(str(file_path))

    # List files in a folder matching a pattern
    def _list_files_in_folder(self, folder_path: str, pattern: str = "*.mp3") -> None:
        folder = Path(folder_path).expanduser().resolve()
        if not folder.is_dir():
            raise ValueError(f"Invalid folder: {folder}")
        print([str(p) for p in folder.glob(pattern) if p.is_file()])
        # return [str(p) for p in folder.glob(pattern) if p.is_file()]
