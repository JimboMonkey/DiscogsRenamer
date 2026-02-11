from pathlib import Path
from pytestqt.qtbot import QtBot

from main_manager import MainManager
from release_data import ReleaseData
from track_data import TrackData

from collections import deque

import pytest


def test_list_audio_files_in_folder(qtbot: QtBot, tmp_path: Path) -> None:
    main_manager = MainManager()

    test_filenames = ["track_1.mp3", "track_2.MP3", "README", "text_file.txt"]

    for filename in test_filenames:
        (tmp_path / filename).touch()

    audio_file_list = main_manager._list_audio_files_in_folder(tmp_path)

    assert [item.original_filename for item in audio_file_list] == [
        "track_1.mp3",
        "track_2.MP3",
    ]


def test_rename_files(qtbot: QtBot, tmp_path: Path) -> None:

    main_manager = MainManager()
    main_window = main_manager._ui

    main_window.set_folder_path_label(str(tmp_path))

    file_renaming_info = [
        ("1", Path("firsttrack.mp3"), Path("First.mp3")),
        ("2", Path("secondtrack.mp3"), Path("Second.mp3")),
        ("3", Path("thirdtrack.mp3"), Path("Third.mp3")),
    ]

    # Create Path objects for original file names
    original_paths = [tmp_path / info[1] for info in file_renaming_info]

    # Create Path objects for new file names
    new_paths = [
        tmp_path / Path(info[0] + " - " + info[2].name) for info in file_renaming_info
    ]

    # Create dummy files in tmp_path
    for pair in file_renaming_info:
        (tmp_path / pair[1]).write_text("dummy content")

    main_manager._rename_files(file_renaming_info)

    for new_path in new_paths:
        assert new_path.exists()

    for original_path in original_paths:
        assert not original_path.exists()


@pytest.fixture
def release_data() -> ReleaseData:
    return ReleaseData(
        release_artists="A Tribe Called Test",
        release_title="Testify",
    )


def test_sanitise_trackdata(qtbot: QtBot, release_data: ReleaseData) -> None:
    main_manager = MainManager()

    track_data = deque(
        [
            TrackData(
                release=release_data,
                track_position="1",
                track_artists='<>:"/\\|?*',
                track_title='<>:"/\\|?*',
            )
        ]
    )

    INVALID_CHARS_REPLACEMENTS: list[tuple[str, str]] = [
        ("<", "("),
        (">", ")"),
        (":", ""),
        ('"', ""),
        ("/", ","),
        ("\\", ","),
        ("|", ","),
        ("?", ""),
        ("*", ""),
    ]
    sanitised_track_data: deque[TrackData] = main_manager._sanitise_trackdata(
        track_data, INVALID_CHARS_REPLACEMENTS
    )

    assert isinstance(sanitised_track_data, deque)
    assert all(isinstance(item, TrackData) for item in sanitised_track_data)

    expected = "(),,,"

    sanitised_track = sanitised_track_data.pop()

    assert sanitised_track.track_artists == expected
    assert sanitised_track.track_title == expected
