from typing import Optional

from PyQt6 import QtGui, QtWidgets

from auth_manager import AuthManager


class Toolbar(QtWidgets.QToolBar):

    def __init__(
        self,
        auth_manager: AuthManager,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._auth_manager = auth_manager

        self._init_ui()

    def _init_ui(self) -> None:
        # Create a New File action
        self.authentication_action = QtGui.QAction(
            QtGui.QIcon("gui/icons/user_authenticated.png"),
            "Authenticate against your Discogs account",
            self,
        )

        # Create a Settings action
        self.settings_action = QtGui.QAction(
            QtGui.QIcon("gui/icons/settings.png"),
            "Settings",
            self,
        )

        # Create an About action
        self.about_action = QtGui.QAction(
            QtGui.QIcon("gui/icons/about.png"),
            "About the application",
            self,
        )

        # Create a file path label and set its font
        user_name_font = QtGui.QFont()
        user_name_font.setBold(True)
        user_name_font.setPointSize(12)

        self.user_name = QtWidgets.QLabel()
        self.user_name.setFont(user_name_font)

        # Set the user before connecting to auth updates
        self.set_user_authenticated_icon(self._auth_manager.user)
        self._auth_manager.user_changed.connect(self.set_user_authenticated_icon)

        # Spacer to push file write button to the right of the toolbar
        toolbar_spacer = QtWidgets.QWidget()
        toolbar_spacer.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )

        # Add all the actions to the tool bar
        self.addAction(self.authentication_action)  # type: ignore[call-overload]
        self.addWidget(self.user_name)
        self.addWidget(toolbar_spacer)
        self.addAction(self.settings_action)  # type: ignore[call-overload]
        self.addAction(self.about_action)  # type: ignore[call-overload]

    # # Called externally to set the file path label
    # def set_file_path_label(self, file_path: Path) -> None:
    #     self.open_file_label.setText(str(file_path))

    def set_user_authenticated_icon(self, auth_user: str | None) -> None:
        if auth_user:
            icon = QtGui.QIcon("gui/icons/user_authenticated.png")
        else:
            icon = QtGui.QIcon("gui/icons/user_unauthenticated.png")
        self.user_name.setText(auth_user)
        self.authentication_action.setIcon(icon)
