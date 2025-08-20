from PyQt6 import QtCore

from gui.main_window import MainWindow


class MainManager(QtCore.QObject):

    def __init__(self) -> None:
        # Create the main GUI window
        self._ui = MainWindow()
        self._ui.show()
