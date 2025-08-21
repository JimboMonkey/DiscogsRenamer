from PyQt6 import QtWidgets
from typing import Optional

from constants import APP_NAME


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(APP_NAME)
