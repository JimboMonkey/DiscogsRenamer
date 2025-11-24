import pytest
from pytestqt.qtbot import QtBot
from gui.tracklist import Tracklist
from collections import deque
from pathlib import Path


@pytest.mark.parametrize(
    "new_filename_test_inputs, ticked_items, expected_response",
    [
        (
            deque(["First", "Second", "Third"]),
            [True, True, True],
            True,
        ),
        (deque(["First", "", "Third"]), [True, True, True], False),
        (
            deque(["First", " ", "Third"]),
            [True, True, True],
            False,
        ),
        (deque(["First", " ", "Third"]), [True, False, True], True),
        (deque(["First", "Second", "Third"]), [False, False, False], False),
    ],
    ids=[
        "all filled, all ticked",
        "one empty, all ticked",
        "one whitespace, all ticked",
        "partially filled, partially ticked",
        "all filled, none ticked",
    ],
)
def test_check_all_new_filenames_filled(
    qtbot: QtBot,
    new_filename_test_inputs: deque[str],
    ticked_items: list[bool],
    expected_response: bool,
) -> None:
    tracklist = Tracklist(editable=True)

    test_tracklist = ["firsttrack", "secondtrack", "thirdtrack"]
    tracklist.populate(test_tracklist)
    tracklist.apply_track_names(new_filename_test_inputs)

    # Tick only the specified items
    for index in range(tracklist.count()):
        tracklist_item = tracklist.itemWidget(tracklist.item(index))
        tracklist_item._checkbox.setChecked(ticked_items[index])

    # qtbot provides a SignalBlocker to capture emissions
    with qtbot.waitSignal(
        tracklist.all_ticked_new_filenames_filled, timeout=1000
    ) as blocker:
        tracklist.check_all_ticked_new_filenames_filled()

    # blocker.args holds the emitted arguments
    assert blocker.args == [expected_response]


@pytest.mark.parametrize(
    "ticked_indices, original_filenames, new_filenames, expected",
    [
        # all ticked → all paths returned
        (
            [True, True, True],
            ["firsttrack", "secondtrack", "thirdtrack"],
            deque(["First", "Second", "Third"]),
            [
                ("1", Path("firsttrack"), Path("First")),
                ("2", Path("secondtrack"), Path("Second")),
                ("3", Path("thirdtrack"), Path("Third")),
            ],
        ),
        # none ticked → None
        (
            [False, False, False],
            ["firsttrack", "secondtrack", "thirdtrack"],
            deque(["First", "Second", "Third"]),
            None,
        ),
        # partial ticked → only ticked ones returned
        (
            [True, False, True],
            ["firsttrack", "secondtrack", "thirdtrack"],
            deque(["First", "Second", "Third"]),
            [
                ("1", Path("firsttrack"), Path("First")),
                ("3", Path("thirdtrack"), Path("Third")),
            ],
        ),
    ],
    ids=["all ticked", "none ticked", "partially ticked"],
)
def test_list_track_renaming_info(
    qtbot: QtBot, ticked_indices, original_filenames, new_filenames, expected
):
    tracklist = Tracklist(editable=True)
    qtbot.addWidget(tracklist)
    tracklist.populate(original_filenames)
    tracklist._number_and_shade()
    tracklist.apply_track_names(new_filenames)

    # Tick only the specified indices
    for i, tick in enumerate(ticked_indices):
        tracklist_item = tracklist.itemWidget(tracklist.item(i))
        tracklist_item._checkbox.setChecked(tick)

    result = tracklist.list_track_renaming_info()
    assert result == expected
