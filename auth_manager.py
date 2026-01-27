from PyQt6 import QtCore


class AuthManager(QtCore.QObject):
    user_changed = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._user: str | None = None

    @property
    def user(self) -> str | None:
        return self._user

    def set_user(self, user: str | None):
        self._user = user
        self.user_changed.emit(user)
