from gui.tracklist_item import TracklistItem
import pytest
from pytestqt.qtbot import QtBot


@pytest.mark.parametrize(
    "new_filename_test_input, expected_response",
    [
        (
            "Test string",
            True,
        ),
        ("", False),
        (" ", False),
    ],
    ids=["filled", "empty", "blank space"],
)
def test_new_filename_filled(
    qtbot: QtBot, new_filename_test_input: str, expected_response: bool
) -> None:
    tracklist_item = TracklistItem()
    qtbot.addWidget(tracklist_item)
    tracklist_item.set_new_filename(new_filename_test_input)
    assert tracklist_item.new_filename_filled() == expected_response


def test_get_track_number(qtbot: QtBot) -> None:
    tracklist_item = TracklistItem()
    qtbot.addWidget(tracklist_item)

    test_track_number = "99"
    tracklist_item.set_track_number(test_track_number)
    assert tracklist_item.get_track_number() == test_track_number


def test_get_new_filename(qtbot: QtBot) -> None:
    tracklist_item = TracklistItem()
    qtbot.addWidget(tracklist_item)

    test_new_filename = "Testing"
    tracklist_item.set_new_filename(test_new_filename)
    assert tracklist_item.get_new_filename() == test_new_filename
