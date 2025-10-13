from gui.main_window import MainWindow
from pytestqt.qtbot import QtBot

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

    line_edit = main_window._release_lineedit
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

    line_edit = main_window._release_lineedit
    validator = line_edit.validator()
    assert validator is not None

    line_edit.setText(invalid_input)
    qtbot.waitSignal(line_edit.textChanged)
    assert not line_edit.hasAcceptableInput()


# Ensure load release button is only enabled when valid text is entered
def test_load_release_button_enabled_by_text(qtbot: QtBot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    line_edit = main_window._release_lineedit
    button = main_window._load_release_button

    # Initially, the button should be disabled
    assert not button.isEnabled()

    # Simulate valid input
    line_edit.setText("[r12345]")
    assert button.isEnabled()
