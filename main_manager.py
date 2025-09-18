from PyQt6 import QtCore, QtWidgets

from gui.main_window import MainWindow

from pathlib import Path
from os.path import expanduser
from typing import List


class MainManager(QtCore.QObject):

    def __init__(self) -> None:
        # Create the main GUI window
        self._ui = MainWindow()
        super(MainManager, self).__init__()

        # Connect signals and slots
        self._ui.file_browser_button.pressed.connect(self._show_open_dialog)

    # Open Folder dialog and return the selected path
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
        folder_path = self._open_dialog()

        # Check for file validity here so that cancelling
        # the open dialog doesn't set a blank path
        if (folder_path) and (Path(folder_path).exists()):
            self._read_folder_contents(Path(folder_path))

    # Set the folder path in the GUI and populate
    # the folder list with the names of its files
    def _read_folder_contents(self, folder_path: Path) -> None:
        self._ui.folder_entry_label.setText(str(folder_path))
        file_list = self._list_audio_files_in_folder(folder_path)
        self._ui.populate_folder_list(file_list)

    # Return a sorted list of audio files in a folder
    def _list_audio_files_in_folder(self, folder_path: Path) -> List[Path]:

        audio_file_extensions = [
            "*.mp3",
            "*.wav",
            "*.flac",
            "*.m4a",
            "*.ogg",
            "*.aiff",
            "*.alac",
            "*.wma",
            "*.aac",
        ]
        return [
            audio_file
            for extension in audio_file_extensions
            for audio_file in sorted(folder_path.glob(extension))
            if audio_file.is_file()
        ]
