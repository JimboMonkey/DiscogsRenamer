from gui.token_dialog_gui import TokenDialogGui
from auth_data_class import AuthenticationResult
from token_manager import TokenManager


class TokenDialog:

    def __init__(self, result: AuthenticationResult) -> None:

        self._token_manager = TokenManager()
        self._ui = TokenDialogGui()
        self._ui.token_lineedit.setText(self._token_manager.load_token())
        self._ui.set_authentication_state(result)

        self._init_connections()

        self._ui.exec()

    # Link GUI widgets to the functions
    def _init_connections(self) -> None:
        self._ui.save_button.clicked.connect(self._save_token)
        self._ui.close_button.clicked.connect(self._ui.close_dialog)

    # Save the token
    def _save_token(self) -> None:
        token = self._ui.token_lineedit.text()
        self._token_manager.save_token(token)
        result = self._token_manager.verify_token(token)
        self._ui.set_authentication_state(result)
