from gui.token_dialog import TokenDialogGui
from pytestqt.qtbot import QtBot

import pytest


# Ensure line edit accepts alphanumeric characters
@pytest.mark.parametrize(
    "valid_input",
    [
        "abc123",  # Letters and digits
        "ABCdef456",  # Mixed case letters and digits
        "abcde",  # Only letters
        "12345",  # Only digits
    ],
)
def test_token_lineedit_accepts_alphanumeric_input(
    qtbot: QtBot, valid_input: str
) -> None:
    dialog = TokenDialogGui()
    qtbot.addWidget(dialog)

    # Check validator exists
    line_edit = dialog._token_lineedit
    validator = line_edit.validator()
    assert validator is not None

    # Valid lineedit input
    line_edit.setText(valid_input)
    qtbot.waitSignal(line_edit.textChanged)
    assert line_edit.hasAcceptableInput()


# Ensure line edit rejects non-alphanumeric characters
@pytest.mark.parametrize(
    "invalid_input",
    [
        "!@#$%",  # Special characters
        "abc 123",  # Space between letters and digits
        "ABC£def456!",  # Mixed case letters, digits, and special characters
    ],
)
def test_token_lineedit_rejects_non_alphanumeric_input(
    qtbot: QtBot, invalid_input: str
) -> None:
    dialog = TokenDialogGui()
    qtbot.addWidget(dialog)

    # Check validator exists
    line_edit = dialog._token_lineedit
    validator = line_edit.validator()
    assert validator is not None

    # Invalid lineedit input
    line_edit.setText(invalid_input)
    qtbot.waitSignal(line_edit.textChanged)
    assert not line_edit.hasAcceptableInput()


# Ensure save button is only enabled when text is entered
def test_save_button_enabled_by_text(qtbot: QtBot):
    dialog = TokenDialogGui()
    qtbot.addWidget(dialog)

    line_edit = dialog._token_lineedit
    button = dialog._save_button

    # Initially, the button should be disabled
    assert not button.isEnabled()

    # Simulate valid input
    line_edit.setText("abc123")
    assert button.isEnabled()
