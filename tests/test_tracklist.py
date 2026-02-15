import pytest
from pytestqt.qtbot import QtBot
from gui.tracklist import Tracklist
from collections import deque
from typing import Callable

from app_settings import AppSettings
from settings_protocol import SettingsProtocol
from gui.filename_list_item import FilenameListItem
from gui.release_list_item import ReleaseListItem
from track_data import TrackData
from release_data import ReleaseData


@pytest.fixture
def app_settings() -> SettingsProtocol:
    return AppSettings()


@pytest.fixture
def release_data() -> ReleaseData:
    return ReleaseData(
        release_artists="A Tribe Called Test",
        release_title="Testify",
    )


@pytest.fixture
def make_new_filename_inputs(release_data: ReleaseData):
    def _make(titles: list[str]):
        items = []
        for i, title in enumerate(titles, start=1):
            items.append(
                ReleaseListItem(
                    TrackData(
                        release=release_data,
                        track_position=str(i),
                        track_artists="A Tribe Called Test",
                        track_title=title,
                    )
                )
            )
        return deque(items)

    return _make


@pytest.mark.parametrize(
    "titles, ticked_items, expected_response",
    [
        (["First", "Second", "Third"], [True, True, True], True),
        (["First", "", "Third"], [True, True, True], False),
        (["First", " ", "Third"], [True, True, True], False),
        (["First", " ", "Third"], [True, False, True], True),
        (["First", "Second", "Third"], [False, False, False], False),
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
    make_new_filename_inputs: Callable[[list[str]], deque[ReleaseListItem]],
    titles: list[str],
    ticked_items: list[bool],
    expected_response: bool,
    app_settings: SettingsProtocol,
):
    new_filename_test_inputs = make_new_filename_inputs(titles)

    # ticked_tracks: deque[TrackData] = deque()
    # ticked_tracks.append(self.item(index).track_data)

    release_tracklist = Tracklist(editable=False, settings=app_settings)
    tracklist = Tracklist(editable=True, settings=app_settings)

    test_tracklist = [
        FilenameListItem("firsttrack"),
        FilenameListItem("secondtrack"),
        FilenameListItem("thirdtrack"),
    ]
    release_tracklist.populate(new_filename_test_inputs)
    tracklist.populate(test_tracklist)

    # Tick only the specified items
    for index in range(tracklist.count()):
        rtracklist_item = release_tracklist.itemWidget(release_tracklist.item(index))
        rtracklist_item._checkbox.setChecked(ticked_items[index])
        tracklist_item = tracklist.itemWidget(tracklist.item(index))
        tracklist_item._checkbox.setChecked(ticked_items[index])

    ticked_track_list = release_tracklist.list_ticked_tracks()

    tracklist.apply_track_names(ticked_track_list, "%title")

    # qtbot provides a SignalBlocker to capture emissions
    with qtbot.waitSignal(
        tracklist.all_ticked_new_filenames_filled, timeout=1000
    ) as blocker:
        tracklist.check_all_ticked_new_filenames_filled()

    # blocker.args holds the emitted arguments
    assert blocker.args == [expected_response]
