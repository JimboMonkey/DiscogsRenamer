import keyring

from constants import APP_NAME, TOKEN_KEY


class TokenManager:
    def load_token(self) -> str | None:
        return keyring.get_password(APP_NAME, TOKEN_KEY)

    def save_token(self, token: str) -> None:
        keyring.set_password(APP_NAME, TOKEN_KEY, token)
