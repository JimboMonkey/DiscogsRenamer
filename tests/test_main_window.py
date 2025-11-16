from main_manager import MainManager
from gui.main_window import MainWindow
from pytestqt.qtbot import QtBot
from collections import deque
from pathlib import Path

import pytest


# Test that the release lineedit accepts valid inputs
@pytest.mark.parametrize(
    "valid_input",
    [
        "12345",  # Only digits
        "r12345",  # r followed by digits
        "[r12345]",  # r followed by bracketed digits
    ],
)
def test_release_lineedit_accepts_valid_inputs(qtbot: QtBot, valid_input: str) -> None:
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    line_edit = main_window.release_lineedit
    validator = line_edit.validator()
    assert validator is not None

    line_edit.setText(valid_input)
    qtbot.waitSignal(line_edit.textChanged)
    assert line_edit.hasAcceptableInput()


# Test that the release lineedit rejects invalid inputs
@pytest.mark.parametrize(
    "invalid_input",
    [
        "abcde",  # Only letters
        "rabcde",  # r followed by letters
        "[rabcde]",  # r followed by bracketed letters
        "r12345abc",  # r followed by digits and letters
        "[r12345abc]",  # r followed by bracketed digits and letters
        "[r12345",  # r followed by unclosed bracket
        "r12345]",  # r followed by unstarted bracket
        "[r12 345]",  # r followed by bracketed digits with space
        "[r!@#$%]",  # r followed by bracketed special characters
    ],
)
def test_release_lineedit_rejects_invalid_inputs(
    qtbot: QtBot, invalid_input: str
) -> None:
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    line_edit = main_window.release_lineedit
    validator = line_edit.validator()
    assert validator is not None

    line_edit.setText(invalid_input)
    qtbot.waitSignal(line_edit.textChanged)
    assert not line_edit.hasAcceptableInput()


# Ensure load release button is only enabled when valid text is entered
def test_load_release_button_enabled_by_text(qtbot: QtBot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    line_edit = main_window.release_lineedit
    button = main_window.load_release_button

    # Initially, the button should be disabled
    assert not button.isEnabled()

    # Simulate valid input
    line_edit.setText("[r12345]")
    assert button.isEnabled()


def test_apply_button_enabled(qtbot: QtBot) -> None:
    main_window = MainWindow()
    qtbot.add_widget(main_window)

    apply_button = main_window.apply_button

    # Initially, the button should be disabled
    assert not apply_button.isEnabled()

    # Simulate true condition
    main_window.apply_button_enabled(True)
    assert apply_button.isEnabled()

    # Simulate false condition
    main_window.apply_button_enabled(False)
    assert not apply_button.isEnabled()


def test_update_release_artist_title_label(qtbot: QtBot) -> None:
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    test_artist = "DJ Test"
    test_title = "Testing The Night Away"

    label = main_window.release_artist_title_label
    main_window.update_release_artist_title_label(test_artist, test_title)
    assert label.text() == f"{test_artist} - {test_title}"


def test_apply_button_enabled_when_all_filenames_populated(qtbot: QtBot) -> None:
    main_manager = MainManager()
    main_window = main_manager._ui
    qtbot.addWidget(main_window)

    test_tracklist = ["One", "Two", "Three"]
    test_new_filenames = deque(["1", "2", "3"])
    main_window.folder_listwidget.populate(test_tracklist)

    # Initially, the button should be disabled
    assert not main_window.apply_button.isEnabled()

    # Simulate valid input
    main_window.folder_listwidget.apply_track_names(test_new_filenames)
    assert main_window.apply_button.isEnabled()


def test_set_folder_path_label(qtbot: QtBot) -> None:

    main_window = MainWindow()
    qtbot.addWidget(main_window)

    test_folder_path = "/test/folder/path"

    main_window.set_folder_path_label(test_folder_path)
    assert main_window.folder_entry_label.text() == test_folder_path


def test_get_folder_path(qtbot: QtBot) -> None:
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    test_folder_path = "/test/folder/path"

    # First check when the folder path hasn't been set yet
    folder_path = main_window.get_folder_path()
    assert folder_path is None

    # Then check once set
    main_window.set_folder_path_label(test_folder_path)
    folder_path = main_window.get_folder_path()
    assert isinstance(folder_path, Path)
    assert folder_path == Path(test_folder_path)
