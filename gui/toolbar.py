from typing import Optional

from PyQt6 import QtGui, QtWidgets


class Toolbar(QtWidgets.QToolBar):

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self) -> None:
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

        # Spacer to push file write button to the right of the toolbar
        toolbar_spacer = QtWidgets.QWidget()
        toolbar_spacer.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )

        # Add all the actions to the tool bar
        self.addWidget(toolbar_spacer)
        self.addAction(self.settings_action)  # type: ignore[call-overload]
        self.addAction(self.about_action)  # type: ignore[call-overload]

    # # Called externally to set the file path label
    # def set_file_path_label(self, file_path: Path) -> None:
    #     self.open_file_label.setText(str(file_path))
