from PyQt6 import QtWidgets
from typing import Optional

from gui.token_dialog import TokenDialogGui

from constants import APP_NAME


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(APP_NAME)
        self.open_token_dialog()

    def open_token_dialog(self) -> None:
        dialog = TokenDialogGui()
        dialog.exec()


# # 🔒 Store the token securely
# def save_token(token: str) -> None:
#     keyring.set_password(APP_NAME, TOKEN_KEY, token)


# # 🔓 Retrieve the token
# def load_token() -> str | None:
#     return keyring.get_password(APP_NAME, TOKEN_KEY)


# # 🧪 Example usage
# if __name__ == "__main__":
#     save_token("sk-1234567890abcdef")
#     token = load_token()
#     print(f"Retrieved token: {token}")


# class TokenWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("API Token")

#         self.input = QLineEdit()
#         self.input.setPlaceholderText("Enter API token")

#         self.save_button = QPushButton("Save Token")
#         self.save_button.clicked.connect(self.save_token)

#         layout = QVBoxLayout()
#         layout.addWidget(self.input)
#         layout.addWidget(self.save_button)
#         self.setLayout(layout)

#         # Load token if available
#         token = load_token()
#         if token:
#             self.input.setText(token)

#     def save_token(self):
#         save_token(self.input.text())
