from PyQt6 import QtCore, QtWidgets

from gui.main_window import MainWindow
from token_dialog import TokenDialog
from token_manager import TokenManager
from discogs_manager import DiscogsManager
from auth_data_class import AuthenticationResult

from pathlib import Path
from os.path import expanduser
from typing import List
from functools import partial


class MainManager(QtCore.QObject):

    def __init__(self) -> None:
        # Create the main GUI window
        self._ui = MainWindow()
        token_manager = TokenManager()
        self._discogs_manager = DiscogsManager()
        super(MainManager, self).__init__()

        # Connect signals and slots
        self._ui.load_release_button.pressed.connect(self._load_release)
        self._ui.file_browser_button.pressed.connect(self._show_open_dialog)
        self._ui.transfer_button.pressed.connect(self._transfer_track_names)
        self._ui.release_listwidget.tick_count.connect(
            partial(self._ui.handle_tick_count, release_tracklist=True)
        )
        self._ui.folder_listwidget.tick_count.connect(
            partial(self._ui.handle_tick_count, release_tracklist=False)
        )

        token = token_manager.load_token()
        # result: AuthenticationResult = token_manager.verify_token(token)
        result = AuthenticationResult(False, None, "Authentication failed")
        # if not result.status:
        #    self.open_token_dialog(result)
        self._ui.toolbar.authentication_action.triggered.connect(
            lambda: self.open_token_dialog(result)
        )


    def extract_digits(self, release_id_string: str) -> int | None:
        digits_string = "".join(
            character for character in release_id_string if character.isdigit()
        )
        return int(digits_string) if digits_string else None

    # Load the release from Discogs and populate the release list
    def _load_release(self) -> None:
        release_id = self.extract_digits(self._ui.release_lineedit.text())
        if release_id:
            release = self._discogs_manager.get_release(release_id)
        if release:
            artist = self._discogs_manager.get_release_artists(release)
            title = self._discogs_manager.get_release_title(release)
            tracklist = self._discogs_manager.get_tracklist(
                release
            )  # [<Track 'A' "I'll Take You There (Remix)">, <Track 'B1' "I'll Take You There (Edit)">, <Track 'B2' 'Wrath Of Kane'>]
            track_titles = self._discogs_manager.get_track_titles(tracklist)
            self._ui.update_release_artist_title_label(artist, title)
            self._ui.release_listwidget.populate(track_titles)

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
        self._ui.folder_listwidget.populate(file_list)

    # Return a sorted list of audio files in a folder
    def _list_audio_files_in_folder(self, folder_path: Path) -> List[str]:

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
            str(audio_file.name)
            for extension in audio_file_extensions
            for audio_file in sorted(folder_path.glob(extension))
            if audio_file.is_file()
        ]

    def open_token_dialog(self, result: AuthenticationResult) -> None:
        _dialog = TokenDialog(result)

    def _transfer_track_names(self):
        ticked_track_list = self._ui.release_listwidget.list_ticked_tracks()
        self._ui.folder_listwidget.apply_track_names(ticked_track_list)
