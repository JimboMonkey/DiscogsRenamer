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
