from PyQt6.QtGui import QValidator
from gui.token_dialog import TokenDialogGui
from pytestqt.qtbot import QtBot


# Ensure line edit only accepts alphanumeric characters
def test_token_lineedit_accepts_only_alphanumeric(qtbot: QtBot):
    dialog = TokenDialogGui()
    qtbot.addWidget(dialog)

    # Check validator exists
    line_edit = dialog._token_lineedit
    validator = line_edit.validator()
    assert validator is not None

    # Valid lineedit input
    validation_result = validator.validate("abc123", 0)[0]
    assert validation_result == QValidator.State.Acceptable

    # Invalid lineedit input
    validation_result = validator.validate("abc123%?!", 0)[0]
    assert validation_result == QValidator.State.Invalid


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
