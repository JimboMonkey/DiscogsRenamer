from PyQt6 import QtGui

from pytestqt.qtbot import QtBot

from gui.toolbar import Toolbar
from auth_manager import AuthManager

import pytest


@pytest.fixture
def auth_manager() -> AuthManager:
    return AuthManager()


def test_set_user_authenticated_icon(qtbot: QtBot, auth_manager: AuthManager):
    toolbar = Toolbar(auth_manager)
    qtbot.addWidget(toolbar)

    authenticated_icon = QtGui.QPixmap("gui/icons/user_authenticated.png").toImage()
    unauthenticated_icon = QtGui.QPixmap("gui/icons/user_unauthenticated.png").toImage()
    test_user = "Test User"

    current_icon = toolbar.authentication_action.icon().pixmap(48, 48).toImage()
    current_user = toolbar.user_name.text()

    # Initially, there should be no authenticated user
    assert current_icon == unauthenticated_icon
    assert current_user == ""

    toolbar.set_user_authenticated_icon(test_user)
    current_icon = toolbar.authentication_action.icon().pixmap(48, 48).toImage()
    current_user = toolbar.user_name.text()

    # After setting a user, the authenticated icon should be set
    assert current_icon == authenticated_icon
    assert current_user == test_user
