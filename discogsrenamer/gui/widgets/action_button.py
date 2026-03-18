from PyQt6 import QtCore, QtGui, QtWidgets


class ActionButton(QtWidgets.QToolButton):
    def __init__(
        self,
        action: QtGui.QAction,
        icon_size: QtCore.QSize = QtCore.QSize(24, 24),
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setDefaultAction(action)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setAutoRaise(True)
        self.setIconSize(icon_size)
