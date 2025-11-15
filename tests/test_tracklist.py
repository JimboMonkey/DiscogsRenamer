import pytest
from pytestqt.qtbot import QtBot
from gui.tracklist import Tracklist
from collections import deque


@pytest.mark.parametrize(
    "new_filename_test_inputs, expected_response",
    [
        (
            deque(["First Track", "Second Track", "Third Track"]),
            True,
        ),
        (deque(["First Track", "", "Third Track"]), False),
        (deque(["First Track", "Second Track", " "]), False),
    ],
    ids=["filled", "empty", "blank space"],
)
def test_check_all_new_filenames_filled(
    qtbot: QtBot, new_filename_test_inputs: deque[str], expected_response: bool
) -> None:
    tracklist = Tracklist(editable=True)

    test_tracklist = ["firsttrack", "secondtrack", "thirdtrack"]
    tracklist.populate(test_tracklist)
    tracklist.apply_track_names(new_filename_test_inputs)

    # qtbot provides a SignalBlocker to capture emissions
    with qtbot.waitSignal(tracklist.all_new_filenames_filled, timeout=1000) as blocker:
        tracklist.check_all_new_filenames_filled()

    # blocker.args holds the emitted arguments
    assert blocker.args == [expected_response]
